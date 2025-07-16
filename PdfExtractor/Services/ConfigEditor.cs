using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using PdfExtractor.Models;

namespace PdfExtractor.Services;

public class ConfigEditor
{
    private readonly Dictionary<string, DocumentTypeConfig> _configs = new();

    public void InitConfig(
        string docType,
        List<string> blocos,
        List<string>? blocosQueIniciamEstrutura = null,
        List<string>? blocosQueUsamDescricao = null
    )
    {
        var config = new DocumentTypeConfig
        {
            Blocos = new Dictionary<string, BlockConfig>(),
            Ignorar = new List<string>()
        };

        foreach (var blocoNome in blocos)
        {
            config.Blocos[blocoNome] = new BlockConfig
            {
                Match = new List<string> { $"^{blocoNome.ToLower()}" },
                FimAoEncontrar = new List<string>(),
                FonteMinima = 14,
                DescricaoFonteMinima = 10,
                IniciaEstrutura = blocosQueIniciamEstrutura?.Contains(blocoNome) == true,
                UsaDescricao = blocosQueUsamDescricao?.Contains(blocoNome) == true
            };
        }

        _configs[docType] = config;
    }

    public void AddIgnore(string docType, List<string> ignorar)
    {
        if (_configs.TryGetValue(docType, out var config))
        {
            config.Ignorar.AddRange(ignorar);
        }
    }

    public void Save(string path)
    {
        var options = new JsonSerializerOptions { WriteIndented = true };
        var json = JsonSerializer.Serialize(_configs, options);
        File.WriteAllText(path, json);
    }
}
