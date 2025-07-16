using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using PdfExtractor.Models;

namespace PdfExtractor.Services;

public class JsonSaver
{
    public static void Save(List<ExtractedStructure> estruturas, string outputDir)
    {
        Directory.CreateDirectory(outputDir);

        for (int i = 0; i < estruturas.Count; i++)
        {
            var estrutura = estruturas[i];
            var nomeArquivo = $"{i + 1:00}_{SanitizeFileName(estrutura.Titulo)}.json";
            var caminho = Path.Combine(outputDir, nomeArquivo);

            var options = new JsonSerializerOptions { WriteIndented = true };
            var json = JsonSerializer.Serialize(estrutura, options);

            File.WriteAllText(caminho, json);
        }
    }

    private static string SanitizeFileName(string input)
    {
        foreach (var c in Path.GetInvalidFileNameChars())
        {
            input = input.Replace(c, '_');
        }
        return input;
    }
}
