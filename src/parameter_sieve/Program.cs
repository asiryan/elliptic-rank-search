using System.Globalization;
using System.Numerics;
using System.Text.Json;

CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
using var cancellation = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cancellation.Cancel(); };
string mode = args.FirstOrDefault() ?? "help";
var options = new Dictionary<string, string>();
for (int i = 1; i < args.Length; i += 2)
{
    if (i + 1 >= args.Length || !args[i].StartsWith("--")) throw new ArgumentException("Use --name value options.");
    options.Add(args[i][2..], args[i + 1]);
}
string Get(string name, string fallback) => options.GetValueOrDefault(name, fallback);
int Number(string name, int fallback, int min, int max)
{
    int n = int.Parse(Get(name, fallback.ToString()));
    if (n < min || n > max) throw new ArgumentOutOfRangeException(name);
    return n;
}
try
{
    if (mode == "sample")
    {
        var cfg = new SampleOptions(Number("samples", 1000000, 1, 100000000), Number("height", 1000000, 1, 1000000000),
            Number("keep", 512, 1, 100000), Number("refine-keep", 64, 1, 10000), Number("final-keep", 24, 1, 1000),
            Number("prime-bound", 65521, 16382, 262139), Number("workers", Math.Min(8, Environment.ProcessorCount), 1, 32),
            Number("seed", 20260914, 0, int.MaxValue));
        if (cfg.FinalKeep > cfg.RefineKeep || cfg.RefineKeep > cfg.Keep) throw new ArgumentException("Require keep >= refine-keep >= final-keep.");
        string selection = Get("selection", "cumulative");
        if (selection == "bands")
            CandidateSampler.RunBands(cfg, Get("output", "runs/parameter-sieve/sample"), cancellation.Token);
        else if (selection == "crt")
            CandidateSampler.RunBands(cfg, Get("output", "runs/parameter-sieve/sample"), cancellation.Token, true);
        else if (selection == "dense")
            CandidateSampler.RunBands(cfg, Get("output", "runs/parameter-sieve/sample"), cancellation.Token, false, true);
        else if (selection == "cumulative")
            CandidateSampler.Run(cfg, Get("output", "runs/parameter-sieve/sample"), cancellation.Token);
        else throw new ArgumentException("Selection must be cumulative, bands, crt or dense.");
    }
    else if (mode == "rescore")
    {
        using var input = JsonDocument.Parse(File.ReadAllText(Get("input", "")));
        var rows = input.RootElement.EnumerateArray().Select(row => new Candidate {
            U = row.GetProperty("u").GetInt32(), V = row.GetProperty("v").GetInt32() }).ToList();
        if (rows.Any(row => row.V <= 0) || rows.Count > 10000) throw new ArgumentException("Invalid rescore candidates.");
        int start = Number("start",65521,0,262138), end = Number("prime-bound",262139,5,262139);
        if (end <= start) throw new ArgumentException("Empty prime interval.");
        Hunt.ScoreStage(rows,start,end,Number("workers",4,1,32),cancellation.Token);
        string output = Get("output","runs/parameter-sieve/rescore.json");
        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(output))!);
        Hunt.Save(output,rows.Select(row => new { u=row.U,v=row.V,score=row.Score,start_exclusive=start,end_inclusive=end }));
    }
    else if (mode == "grid")
    {
        var cfg = new HuntOptions(Number("height", 10000, 1, 1000000), Number("keep", 8192, 1, 100000),
            Number("refine-keep", 256, 1, 10000), Number("final-keep", 48, 1, 1000),
            Number("prime-bound", 65521, 16382, 262139), Number("workers", Math.Min(4, Environment.ProcessorCount), 1, 32));
        if (cfg.FinalKeep > cfg.RefineKeep || cfg.RefineKeep > cfg.Keep) throw new ArgumentException("Require keep >= refine-keep >= final-keep.");
        Hunt.Run(cfg, Get("output", "runs/parameter-sieve/grid"), cancellation.Token);
    }
    else if (mode == "help") Console.WriteLine("ParameterSieve grid|sample|rescore [--name value ...]; see README.md");
    else throw new ArgumentException("Unknown mode. Use grid, sample or rescore.");
}
catch (OperationCanceledException) { Console.WriteLine("Stopped. Completed grid batches are checkpointed; rerun with the same options."); }
catch (Exception error)
{
    Console.Error.WriteLine($"RankHunt failed: {error.Message}");
    Environment.ExitCode = 1;
}
