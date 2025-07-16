using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using PdfExtractor.Models;

namespace PdfExtractor.Services
{
    public class ConfigLoader
    {
        public DocumentTypeConfig Load(string path, string docTypeKey)
        {
            if (!File.Exists(path))
                throw new FileNotFoundException($"Arquivo de configuração não encontrado: {path}");

            string jsonContent = File.ReadAllText(path);

            // Deserialize o JSON para o dicionário que contém várias configs
            var raw = JsonSerializer.Deserialize<Dictionary<string, DocumentTypeConfig>>(jsonContent);

            if (raw == null || !raw.TryGetValue(docTypeKey, out var config))
                throw new InvalidOperationException($"Configuração '{docTypeKey}' não encontrada no JSON.");

            PrecompileRegex(config);

            return config;
        }

        // Para produção, tornar privado
        public void PrecompileRegex(DocumentTypeConfig config)
        {
            foreach (var bloco in config.Blocos.Values)
            {
                bloco.CompiledPatterns = new List<Regex>();

                if (bloco.Match != null)
                {
                    foreach (var pattern in bloco.Match)
                    {
                        var regex = new Regex(pattern, RegexOptions.IgnoreCase | RegexOptions.Compiled);
                        bloco.CompiledPatterns.Add(regex);
                    }
                }

                if (bloco.FimAoEncontrar != null)
                {
                    for (int i = 0; i < bloco.FimAoEncontrar.Count; i++)
                    {
                        bloco.FimAoEncontrar[i] = bloco.FimAoEncontrar[i].Trim().ToLower();
                    }
                }
            }
        }
    }
}
