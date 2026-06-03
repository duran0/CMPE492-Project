Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$comsolBin = "C:\Program Files\COMSOL\COMSOL62\Multiphysics\bin\win64"
$compile = Join-Path $comsolBin "comsolcompile.exe"
$batch = Join-Path $comsolBin "comsolbatch.exe"

if (-not (Test-Path $compile)) {
    throw "COMSOL compiler not found at $compile"
}
if (-not (Test-Path $batch)) {
    throw "COMSOL batch executable not found at $batch"
}

$models = @(
    @{ Source="comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.java"; Output="comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph"; Log="comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.log" },
    @{ Source="comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.java"; Output="comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.mph"; Log="comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.log" },
    @{ Source="comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.java"; Output="comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.mph"; Log="comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.log" },
    @{ Source="comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.java"; Output="comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.mph"; Log="comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.log" },
    @{ Source="comsol/models/M4_gfet_response/M4_gfet_current_response_v01.java"; Output="comsol/models/M4_gfet_response/M4_gfet_current_response_v01.mph"; Log="comsol/models/M4_gfet_response/M4_gfet_current_response_v01.log" }
)

foreach ($model in $models) {
    $source = Join-Path $root $model.Source
    $output = Join-Path $root $model.Output
    $log = Join-Path $root $model.Log
    $class = [System.IO.Path]::ChangeExtension($source, ".class")
    $status = "$class.status"

    Remove-Item -Force $class, $status, $output, $log -ErrorAction SilentlyContinue
    & $compile $source
    if (-not (Test-Path $class)) {
        throw "Compilation failed for $source"
    }
    & $batch -inputfile $class -outputfile $output -batchlog $log
    if (-not (Test-Path $output)) {
        $fallback = Join-Path (Split-Path -Parent $source) (([System.IO.Path]::GetFileNameWithoutExtension($source)) + "_Model.mph")
        if (Test-Path $fallback) {
            Move-Item -Force $fallback $output
        }
    }
    if (-not (Test-Path $output)) {
        throw "COMSOL output file was not produced: $output"
    }
    Write-Output "Built $($model.Output)"
}
