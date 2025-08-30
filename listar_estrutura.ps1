# Como utilizar:
# 1. Abra o powershell
# 2. Entre no diretório onde o script está localizado
# 3. Execute `powershell -ExecutionPolicy Bypass -File listar_estrutura.ps1 > estrutura.txt`
# Isso irá atualizar o arquivo "estrutura.txt" com toda a estrutura dentro do diretório.
function Show-Tree {
    param (
        [string]$Path = ".",
        [int]$Level = 0
    )

    $prefix = "|   " * $Level + "|-- "

    Get-ChildItem -LiteralPath $Path -Force | Where-Object {
        -not ($_.Name -in @('__pycache__', '.venv', '.git')) -and
        -not ($_.Name -like '*.pyc')
    } | Sort-Object { -not $_.PSIsContainer }, Name | ForEach-Object {
        Write-Output "$prefix$($_.Name)"
        if ($_.PSIsContainer) {
            Show-Tree -Path $_.FullName -Level ($Level + 1)
        }
    }
}

Show-Tree "." 0
