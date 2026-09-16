$ErrorActionPreference = "Stop"

[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

$imagePath = "c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\temp_p1.png"

# First ensure temp_p1.png is created by python
$pyScript = @"
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument(r'$($imagePath.Replace("temp_p1.png", "Alandas_B2B.pdf"))')
img = pdf[0].render(scale=2).to_pil()
img.save(r'$imagePath')
print('Page 1 rendered!')
"@
python -c $pyScript

# Helper function to await WinRT async operation
function Await-Async ($asyncOp) {
    while ($asyncOp.Status -eq [Windows.Foundation.AsyncStatus]::Started) {
        Start-Sleep -Milliseconds 20
    }
    if ($asyncOp.Status -eq [Windows.Foundation.AsyncStatus]::Completed) {
        return $asyncOp.GetResults()
    } else {
        throw "Async operation failed: $($asyncOp.ErrorCode)"
    }
}

$fileOp = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath)
$file = Await-Async $fileOp

$streamOp = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
$stream = Await-Async $streamOp

$decoderOp = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
$decoder = Await-Async $decoderOp

$bitmapOp = $decoder.GetSoftwareBitmapAsync()
$bitmap = Await-Async $bitmapOp

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) {
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new("en-US"))
}

$ocrOp = $engine.RecognizeAsync($bitmap)
$result = Await-Async $ocrOp

Write-Host "=== OCR RESULT FOR PAGE 1 ==="
Write-Host $result.Text
