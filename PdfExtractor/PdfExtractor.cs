using System.Collections.Generic;
using PdfExtractor.Models;
using PdfExtractor.Services;

namespace PdfExtractor
{
    public class PdfExtractor
    {
        private readonly DocumentTypeConfig _docTypeConfig;

        // Alterado para receber docTypeKey
        public PdfExtractor(string docTypeConfigPath, string docTypeKey)
        {
            var loader = new ConfigLoader();
            _docTypeConfig = loader.Load(docTypeConfigPath, docTypeKey);
        }

        public List<ExtractedStructure> ExtractBatch(List<string> pdfPaths, string outputDir)
        {
            var processor = new PdfProcessor(_docTypeConfig);
            var todasEstruturas = new List<ExtractedStructure>();

            foreach (var pdfPath in pdfPaths)
            {
                var estruturas = processor.Extract(pdfPath);
                todasEstruturas.AddRange(estruturas);
            }

            JsonSaver.Save(todasEstruturas, outputDir);

            return todasEstruturas;
        }
    }
}
