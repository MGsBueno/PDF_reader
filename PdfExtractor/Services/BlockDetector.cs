using System;
using PdfExtractor.Models;

namespace PdfExtractor.Services
{
    public class BlockDetector
    {
        private readonly DocumentTypeConfig _docTypeConfig;

        public BlockDetector(DocumentTypeConfig docTypeConfig)
        {
            _docTypeConfig = docTypeConfig;
        }

        public string? DetectarBloco(string texto, double fonte)
        {
            foreach (var blocoKvp in _docTypeConfig.Blocos)
            {
                string nomeBloco = blocoKvp.Key;
                BlockConfig bloco = blocoKvp.Value;

                foreach (var pattern in bloco.CompiledPatterns)
                {
                    bool isMatch = pattern.IsMatch(texto);
                    
                    if (isMatch && fonte >= bloco.FonteMinima)
                        return nomeBloco;
                }
            }
            return null;
        }

    }
}
