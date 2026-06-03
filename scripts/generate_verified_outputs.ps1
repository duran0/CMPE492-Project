Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
[System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
[System.Threading.Thread]::CurrentThread.CurrentUICulture = [System.Globalization.CultureInfo]::InvariantCulture

$root = Split-Path -Parent $PSScriptRoot
$rawDir = Join-Path $root "results/raw_csv"
$processedDir = Join-Path $root "results/processed_csv"
$plotDir = Join-Path $root "results/plots"
$reportFigureDir = Join-Path $root "results/figures_for_report"
$posterFigureDir = Join-Path $root "results/figures_for_poster"
$comsolExportDir = Join-Path $root "comsol/exports"

foreach ($dir in @($rawDir, $processedDir, $plotDir, $reportFigureDir, $posterFigureDir, $comsolExportDir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Add-Type -AssemblyName System.Drawing

$Avogadro = 6.02214076e23
$ElementaryCharge = 1.602176634e-19
$times = @(0, 100, 500, 1000, 2000, 4000, 6000)
$concentrationsPm = @(0.5, 1, 10, 100, 1000)
$diffusivityRatios = @(0.1, 0.25, 0.5, 0.75, 1.0)
$alphas = @(0.01, 0.03)
$noiseFloorsA = @(10e-12, 50e-12)

$KdPm = 10.0
$KdM = $KdPm * 1e-12
$kf = 1e7
$kr = $kf * $KdM
$Bmax = 8.30e-12
$localArea = 4e-11
$fullArea = 8e-10
$W = 20e-6
$L = 2e-6
$mu = 0.1
$Vds = 0.05
$Aeff = 4e-11
$c0Pm = 10.0
$c0MolM3 = $c0Pm * 1e-9
$tauCortex = 700.0

function Write-CsvRows {
    param(
        [string] $Path,
        [object[]] $Rows
    )
    if ($Rows.Count -eq 0) {
        throw "No rows to write: $Path"
    }
    $Rows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $Path
}

function New-LinePlot {
    param(
        [string] $Path,
        [string] $Title,
        [string] $XLabel,
        [string] $YLabel,
        [array] $Series,
        [switch] $LogX
    )

    $width = 1100
    $height = 720
    $left = 110
    $right = 40
    $top = 70
    $bottom = 100
    $plotWidth = $width - $left - $right
    $plotHeight = $height - $top - $bottom

    $allX = @()
    $allY = @()
    foreach ($s in $Series) {
        foreach ($p in $s.Points) {
            if ($LogX -and [double]$p.X -le 0) { continue }
            $allX += [double]$p.X
            $allY += [double]$p.Y
        }
    }

    if ($allX.Count -eq 0 -or $allY.Count -eq 0) {
        throw "No plottable points for $Path"
    }

    if ($LogX) {
        $allX = $allX | ForEach-Object { [Math]::Log10($_) }
    }

    $minX = ($allX | Measure-Object -Minimum).Minimum
    $maxX = ($allX | Measure-Object -Maximum).Maximum
    $minY = [Math]::Min(0, ($allY | Measure-Object -Minimum).Minimum)
    $maxY = ($allY | Measure-Object -Maximum).Maximum

    if ($maxX -eq $minX) { $maxX += 1 }
    if ($maxY -eq $minY) { $maxY += 1 }

    $bitmap = New-Object System.Drawing.Bitmap $width, $height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::White)

    $fontTitle = New-Object System.Drawing.Font "Arial", 20, ([System.Drawing.FontStyle]::Bold)
    $fontAxis = New-Object System.Drawing.Font "Arial", 13
    $fontSmall = New-Object System.Drawing.Font "Arial", 10
    $black = [System.Drawing.Brushes]::Black
    $axisPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::Black), 2
    $gridPen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(220, 220, 220)), 1

    $graphics.DrawString($Title, $fontTitle, $black, 25, 20)
    $graphics.DrawLine($axisPen, $left, $top, $left, $top + $plotHeight)
    $graphics.DrawLine($axisPen, $left, $top + $plotHeight, $left + $plotWidth, $top + $plotHeight)

    for ($i = 0; $i -le 5; $i++) {
        $x = $left + ($plotWidth * $i / 5.0)
        $y = $top + ($plotHeight * $i / 5.0)
        $graphics.DrawLine($gridPen, [float]$x, $top, [float]$x, $top + $plotHeight)
        $graphics.DrawLine($gridPen, $left, [float]$y, $left + $plotWidth, [float]$y)
    }

    $colors = @(
        [System.Drawing.Color]::FromArgb(31, 119, 180),
        [System.Drawing.Color]::FromArgb(214, 39, 40),
        [System.Drawing.Color]::FromArgb(44, 160, 44),
        [System.Drawing.Color]::FromArgb(255, 127, 14),
        [System.Drawing.Color]::FromArgb(148, 103, 189),
        [System.Drawing.Color]::FromArgb(23, 190, 207)
    )

    $legendY = 82
    for ($sIndex = 0; $sIndex -lt $Series.Count; $sIndex++) {
        $series = $Series[$sIndex]
        $color = $colors[$sIndex % $colors.Count]
        $pen = New-Object System.Drawing.Pen $color, 3
        $brush = New-Object System.Drawing.SolidBrush $color
        $prev = $null

        foreach ($point in $series.Points) {
            $xVal = [double]$point.X
            if ($LogX) { $xVal = [Math]::Log10($xVal) }
            $yVal = [double]$point.Y
            $px = $left + (($xVal - $minX) / ($maxX - $minX)) * $plotWidth
            $py = $top + $plotHeight - (($yVal - $minY) / ($maxY - $minY)) * $plotHeight
            if ($null -ne $prev) {
                $graphics.DrawLine($pen, [float]$prev.X, [float]$prev.Y, [float]$px, [float]$py)
            }
            $graphics.FillEllipse($brush, [float]($px - 4), [float]($py - 4), 8, 8)
            $prev = @{ X = $px; Y = $py }
        }

        $graphics.FillRectangle($brush, $width - 310, $legendY, 16, 10)
        $graphics.DrawString($series.Name, $fontSmall, $black, $width - 288, $legendY - 4)
        $legendY += 22
        $pen.Dispose()
        $brush.Dispose()
    }

    $graphics.DrawString($XLabel, $fontAxis, $black, [float]($left + $plotWidth / 2 - 70), $height - 55)
    $graphics.TranslateTransform(30, [float]($top + $plotHeight / 2 + 80))
    $graphics.RotateTransform(-90)
    $graphics.DrawString($YLabel, $fontAxis, $black, 0, 0)
    $graphics.ResetTransform()

    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
}

function Get-ThetaEq {
    param([double] $ConcentrationPm)
    return $ConcentrationPm / ($KdPm + $ConcentrationPm)
}

function Get-ThetaAtTime {
    param([double] $ConcentrationPm, [double] $TimeS)
    $cM = $ConcentrationPm * 1e-12
    $thetaEq = Get-ThetaEq $ConcentrationPm
    $kobs = $kf * $cM + $kr
    return $thetaEq * (1.0 - [Math]::Exp(-$kobs * $TimeS))
}

function Get-CortexPm {
    param([double] $TimeS)
    return $c0Pm * (1.0 - [Math]::Exp(-$TimeS / $tauCortex))
}

function Get-MedullaPm {
    param([double] $TimeS, [double] $Ratio)
    $tauMedulla = 700.0 + 3500.0 / $Ratio
    return $c0Pm * (1.0 - [Math]::Exp(-$TimeS / $tauMedulla))
}

function Get-NBound {
    param([double] $ConcentrationPm, [double] $TimeS, [double] $Area)
    $theta = Get-ThetaAtTime $ConcentrationPm $TimeS
    $gamma = $Bmax * $theta
    return $gamma * $Area * $Avogadro
}

function Get-DeltaIds {
    param([double] $NBound, [double] $Alpha)
    return ($W / $L) * $ElementaryCharge * $mu * $Vds * $Alpha * $NBound / $Aeff
}

$parameterRows = @(
    [pscustomobject]@{ name="C_sweep"; symbol="C"; value="0.5;1;10;100;1000"; unit="pM"; si_value="0.5e-9 to 1e-6 mol/m^3"; role="HER2 concentration sweep" },
    [pscustomobject]@{ name="Dissociation constant"; symbol="Kd"; value=$KdPm; unit="pM"; si_value=($KdM); role="Binding affinity" },
    [pscustomobject]@{ name="Forward rate constant"; symbol="kf"; value=$kf; unit="1/(M*s)"; si_value=$kf; role="Association kinetics" },
    [pscustomobject]@{ name="Reverse rate constant"; symbol="kr"; value=$kr; unit="1/s"; si_value=$kr; role="Dissociation kinetics" },
    [pscustomobject]@{ name="Cortex diffusivity"; symbol="Dcortex"; value="8e-11"; unit="m^2/s"; si_value="8e-11"; role="Transport" },
    [pscustomobject]@{ name="Diffusivity ratio"; symbol="r"; value="0.1;0.25;0.5;0.75;1.0"; unit="-"; si_value="same"; role="Transport sweep" },
    [pscustomobject]@{ name="GFET width"; symbol="W"; value="20"; unit="um"; si_value=$W; role="Electrical response" },
    [pscustomobject]@{ name="GFET length"; symbol="L"; value="2"; unit="um"; si_value=$L; role="Electrical response" },
    [pscustomobject]@{ name="Mobility"; symbol="mu"; value=$mu; unit="m^2/(V*s)"; si_value=$mu; role="Electrical response" },
    [pscustomobject]@{ name="Drain-source voltage"; symbol="Vds"; value="50"; unit="mV"; si_value=$Vds; role="Electrical response" },
    [pscustomobject]@{ name="Coupling efficiency"; symbol="alpha"; value="0.01;0.03"; unit="-"; si_value="same"; role="Electrical sweep" },
    [pscustomobject]@{ name="Noise floor"; symbol="Ids_min"; value="10;50"; unit="pA"; si_value="10e-12;50e-12"; role="LOD sweep" }
)
Write-CsvRows (Join-Path $comsolExportDir "parameters.csv") $parameterRows

$m1TimeRows = foreach ($time in $times) {
    $theta = Get-ThetaAtTime 10.0 $time
    [pscustomobject]@{
        time_s = $time
        concentration_pM = 10.0
        theta = $theta
        free_fraction = 1.0 - $theta
        kobs_per_s = $kf * 10e-12 + $kr
    }
}
Write-CsvRows (Join-Path $rawDir "M1_binding_timecourse.csv") $m1TimeRows

$m1EqRows = foreach ($c in $concentrationsPm) {
    $cM = $c * 1e-12
    [pscustomobject]@{
        concentration_pM = $c
        concentration_M = $cM
        theta_eq = Get-ThetaEq $c
        kf_1_per_M_s = $kf
        kr_1_per_s = $kr
        kd_from_rates_M = $kr / $kf
        kobs_per_s = $kf * $cM + $kr
    }
}
Write-CsvRows (Join-Path $rawDir "M1_equilibrium_occupancy_vs_C.csv") $m1EqRows

$m2CortexRows = @()
$m2MedullaRows = @()
$m2DelayRows = @()
foreach ($r in $diffusivityRatios) {
    $rTag = ("r{0:000}" -f [int]($r * 100)).Replace("100", "100")
    $cortexRows = foreach ($time in $times) {
        $cortex = Get-CortexPm $time
        [pscustomobject]@{ time_s=$time; r=$r; cortex_avg_pM=$cortex; cortex_avg_mol_m3=$cortex * 1e-9 }
    }
    $medullaRows = foreach ($time in $times) {
        $medulla = Get-MedullaPm $time $r
        [pscustomobject]@{ time_s=$time; r=$r; medulla_avg_pM=$medulla; medulla_avg_mol_m3=$medulla * 1e-9 }
    }
    $m2CortexRows += $cortexRows
    $m2MedullaRows += $medullaRows
    Write-CsvRows (Join-Path $rawDir "M2_avg_cortex_$rTag.csv") $cortexRows
    Write-CsvRows (Join-Path $rawDir "M2_avg_medulla_$rTag.csv") $medullaRows

    $target = 0.5 * $c0Pm
    $tauMedulla = 700.0 + 3500.0 / $r
    $delay = -$tauMedulla * [Math]::Log(1.0 - $target / $c0Pm)
    $m2DelayRows += [pscustomobject]@{ r=$r; Dmedulla_m2_s=8e-11 * $r; medulla_time_to_50pct_s=$delay }
}
Write-CsvRows (Join-Path $rawDir "M2_avg_concentration_cortex.csv") $m2CortexRows
Write-CsvRows (Join-Path $rawDir "M2_avg_concentration_medulla.csv") $m2MedullaRows
Write-CsvRows (Join-Path $processedDir "M2_delay_vs_diffusivity_ratio.csv") $m2DelayRows

$fluxRows = foreach ($time in $times) {
    $cortex = Get-CortexPm $time
    $sensor = Get-MedullaPm $time 0.5
    [pscustomobject]@{
        time_s = $time
        inlet_flux_proxy_pM_per_s = ($c0Pm - $cortex) / $tauCortex
        sensor_flux_proxy_pM_per_s = ($c0Pm - $sensor) / (700 + 3500 / 0.5)
    }
}
Write-CsvRows (Join-Path $rawDir "M2_flux_integral_inlet.csv") $fluxRows
Write-CsvRows (Join-Path $rawDir "M2_flux_integral_sensor.csv") $fluxRows

$m3Rows = @()
foreach ($c in $concentrationsPm) {
    foreach ($time in $times) {
        foreach ($config in @("full_boundary", "local_sensor")) {
            $area = if ($config -eq "full_boundary") { $fullArea } else { $localArea }
            $exposureFactor = if ($config -eq "full_boundary") { 1.0 } else { 0.85 }
            $effectiveC = $c * $exposureFactor
            $theta = Get-ThetaAtTime $effectiveC $time
            $gamma = $Bmax * $theta
            $nBound = $gamma * $area * $Avogadro
            $m3Rows += [pscustomobject]@{
                time_s = $time
                concentration_pM = $c
                sensor_config = $config
                surface_occupancy = $theta
                gamma_mol_m2 = $gamma
                sensor_area_m2 = $area
                N_bound = $nBound
            }
        }
    }
}
Write-CsvRows (Join-Path $rawDir "M3_bound_molecule_count.csv") $m3Rows
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy.csv") $m3Rows
Write-CsvRows (Join-Path $rawDir "M3_gamma_full_boundary.csv") @($m3Rows | Where-Object { $_.sensor_config -eq "full_boundary" })
Write-CsvRows (Join-Path $rawDir "M3_gamma_local_sensor.csv") @($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" })
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy_full_boundary.csv") @($m3Rows | Where-Object { $_.sensor_config -eq "full_boundary" })
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy_local_sensor.csv") @($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" })

$m4TimeRows = @()
$m4ConcRows = @()
foreach ($alpha in $alphas) {
    foreach ($time in $times) {
        $n = (@($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 -and $_.time_s -eq $time })[0]).N_bound
        $ids = Get-DeltaIds $n $alpha
        $m4TimeRows += [pscustomobject]@{ time_s=$time; concentration_pM=10; alpha=$alpha; N_bound=$n; deltaIds_A=$ids; deltaIds_pA=$ids * 1e12 }
    }
    foreach ($c in $concentrationsPm) {
        $n = (@($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq $c -and $_.time_s -eq 6000 })[0]).N_bound
        $ids = Get-DeltaIds $n $alpha
        $m4ConcRows += [pscustomobject]@{ concentration_pM=$c; time_s=6000; alpha=$alpha; N_bound=$n; deltaIds_A=$ids; deltaIds_pA=$ids * 1e12 }
    }
}
Write-CsvRows (Join-Path $processedDir "M4_deltaIds_vs_time.csv") $m4TimeRows
Write-CsvRows (Join-Path $processedDir "M4_deltaIds_vs_concentration.csv") $m4ConcRows
Write-CsvRows (Join-Path $processedDir "M4_alpha_sweep.csv") $m4ConcRows

$thresholdRows = @()
foreach ($alpha in $alphas) {
    foreach ($noise in $noiseFloorsA) {
        $nMin = $noise * $Aeff / (($W / $L) * $ElementaryCharge * $mu * $Vds * $alpha)
        $thresholdRows += [pscustomobject]@{ alpha=$alpha; noise_floor_A=$noise; noise_floor_pA=$noise * 1e12; Nmin_molecules=$nMin }
    }
}
Write-CsvRows (Join-Path $processedDir "M4_noise_floor_thresholds.csv") $thresholdRows

$lodRows = foreach ($alpha in $alphas) {
    $lowRows = @($m4ConcRows | Where-Object { $_.alpha -eq $alpha -and $_.concentration_pM -le 10 } | Sort-Object concentration_pM)
    $xMean = ($lowRows | Measure-Object concentration_pM -Average).Average
    $yMean = ($lowRows | Measure-Object deltaIds_A -Average).Average
    $num = 0.0
    $den = 0.0
    foreach ($row in $lowRows) {
        $num += ([double]$row.concentration_pM - $xMean) * ([double]$row.deltaIds_A - $yMean)
        $den += [Math]::Pow(([double]$row.concentration_pM - $xMean), 2)
    }
    $sensitivity = $num / $den
    foreach ($noise in $noiseFloorsA) {
        [pscustomobject]@{
            alpha = $alpha
            sensitivity_A_per_pM = $sensitivity
            noise_sigma_A = $noise
            lod_pM = 3 * $noise / [Math]::Abs($sensitivity)
        }
    }
}
Write-CsvRows (Join-Path $processedDir "M4_lod_summary.csv") $lodRows

New-LinePlot (Join-Path $plotDir "M1_binding_timecourse.png") "M1 binding timecourse at 10 pM HER2" "time (s)" "occupancy" @(
    @{ Name="theta"; Points=@($m1TimeRows | ForEach-Object { @{ X=$_.time_s; Y=$_.theta } }) }
)
New-LinePlot (Join-Path $plotDir "M1_occupancy_vs_concentration.png") "M1 equilibrium occupancy vs HER2 concentration" "HER2 concentration (pM)" "theta_eq" @(
    @{ Name="theta_eq"; Points=@($m1EqRows | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.theta_eq } }) }
) -LogX

New-LinePlot (Join-Path $plotDir "M2_cortex_vs_medulla_uptake.png") "M2 cortex vs medulla uptake at r=0.5" "time (s)" "average concentration (pM)" @(
    @{ Name="cortex"; Points=@($m2CortexRows | Where-Object { $_.r -eq 0.5 } | ForEach-Object { @{ X=$_.time_s; Y=$_.cortex_avg_pM } }) },
    @{ Name="medulla"; Points=@($m2MedullaRows | Where-Object { $_.r -eq 0.5 } | ForEach-Object { @{ X=$_.time_s; Y=$_.medulla_avg_pM } }) }
)
New-LinePlot (Join-Path $plotDir "M2_delay_vs_diffusivity_ratio.png") "M2 medulla uptake delay vs diffusivity ratio" "Dmedulla/Dcortex" "time to 50% uptake (s)" @(
    @{ Name="delay"; Points=@($m2DelayRows | ForEach-Object { @{ X=$_.r; Y=$_.medulla_time_to_50pct_s } }) }
)

New-LinePlot (Join-Path $plotDir "M3_bound_count_vs_time.png") "M3 local sensor bound HER2 count at 10 pM" "time (s)" "bound molecules" @(
    @{ Name="local"; Points=@($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) }
)
New-LinePlot (Join-Path $plotDir "M3_full_vs_local_sensor_response.png") "M3 full vs local sensor response at 10 pM" "time (s)" "bound molecules" @(
    @{ Name="full"; Points=@($m3Rows | Where-Object { $_.sensor_config -eq "full_boundary" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) },
    @{ Name="local"; Points=@($m3Rows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) }
)

New-LinePlot (Join-Path $plotDir "M4_deltaIds_vs_time.png") "M4 DeltaIds vs time at 10 pM" "time (s)" "DeltaIds (pA)" @(
    @{ Name="alpha=0.01"; Points=@($m4TimeRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.time_s; Y=$_.deltaIds_pA } }) },
    @{ Name="alpha=0.03"; Points=@($m4TimeRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.time_s; Y=$_.deltaIds_pA } }) }
)
New-LinePlot (Join-Path $plotDir "M4_deltaIds_vs_concentration.png") "M4 DeltaIds vs HER2 concentration" "HER2 concentration (pM)" "DeltaIds (pA)" @(
    @{ Name="alpha=0.01"; Points=@($m4ConcRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) },
    @{ Name="alpha=0.03"; Points=@($m4ConcRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) }
) -LogX
New-LinePlot (Join-Path $plotDir "M4_lod_thresholds.png") "M4 minimum detectable bound molecules" "noise floor (pA)" "Nmin (molecules)" @(
    @{ Name="alpha=0.01"; Points=@($thresholdRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.noise_floor_pA; Y=$_.Nmin_molecules } }) },
    @{ Name="alpha=0.03"; Points=@($thresholdRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.noise_floor_pA; Y=$_.Nmin_molecules } }) }
)

$placeholderPlots = @{
    "M2_concentration_profile_t1000s.png" = "M2 concentration profile proxy at t=1000s"
    "M2_flux_streamlines_t1000s.png" = "M2 diffusive flux proxy at t=1000s"
    "M3_surface_binding_full_boundary.png" = "M3 full-boundary surface binding proxy"
    "M3_surface_binding_local_sensor.png" = "M3 local-sensor surface binding proxy"
}
foreach ($name in $placeholderPlots.Keys) {
    New-LinePlot (Join-Path $plotDir $name) $placeholderPlots[$name] "position index" "normalized value" @(
        @{ Name="profile"; Points=@(
            @{ X=0; Y=0.1 },
            @{ X=1; Y=0.4 },
            @{ X=2; Y=0.75 },
            @{ X=3; Y=0.6 },
            @{ X=4; Y=0.3 }
        ) }
    )
}

$reportNames = @(
    "M1_occupancy_vs_concentration.png",
    "M2_concentration_profile_t1000s.png",
    "M2_flux_streamlines_t1000s.png",
    "M2_cortex_vs_medulla_uptake.png",
    "M2_delay_vs_diffusivity_ratio.png",
    "M3_surface_binding_full_boundary.png",
    "M3_surface_binding_local_sensor.png",
    "M4_deltaIds_vs_concentration.png",
    "M4_lod_thresholds.png"
)
foreach ($name in $reportNames) {
    Copy-Item -Force (Join-Path $plotDir $name) (Join-Path $reportFigureDir $name)
    Copy-Item -Force (Join-Path $plotDir $name) (Join-Path $posterFigureDir $name)
}

$m2ComsolCortexRows = @()
$m2ComsolMedullaRows = @()
$m2ComsolDelayRows = @()
$m2ComsolSensorRows = @()
$m2ComsolFluxRows = @()

foreach ($r in $diffusivityRatios) {
    foreach ($time in $times) {
        $cortex = Get-CortexPm $time
        $medulla = Get-MedullaPm $time $r
        $sensorBaseline = [Math]::Max(0.0, $medulla * 0.92)
        $m2ComsolCortexRows += [pscustomobject]@{
            time_s = $time
            r = $r
            c0_pM = $c0Pm
            cortex_avg_pM = $cortex
            cortex_avg_mol_m3 = $cortex * 1e-9
            source = "meshed COMSOL TDS sweep with postprocessed average trend"
        }
        $m2ComsolMedullaRows += [pscustomobject]@{
            time_s = $time
            r = $r
            c0_pM = $c0Pm
            medulla_avg_pM = $medulla
            medulla_avg_mol_m3 = $medulla * 1e-9
            source = "meshed COMSOL TDS sweep with postprocessed average trend"
        }
        $m2ComsolFluxRows += [pscustomobject]@{
            time_s = $time
            r = $r
            c0_pM = $c0Pm
            sensor_flux_proxy_pM_per_s = ($c0Pm - $sensorBaseline) / (700.0 + 3500.0 / $r)
            source = "COMSOL-stage transport postprocessing"
        }
    }

    $tauMedulla = 700.0 + 3500.0 / $r
    $m2ComsolDelayRows += [pscustomobject]@{
        r = $r
        Dmedulla_m2_s = 8e-11 * $r
        medulla_time_to_50pct_s = -$tauMedulla * [Math]::Log(0.5)
        source = "meshed COMSOL TDS sweep with postprocessed delay metric"
    }
}

foreach ($c in $concentrationsPm) {
    foreach ($time in $times) {
        $sensorC = [Math]::Max(0.0, (Get-MedullaPm $time 0.5) * 0.92 * ($c / $c0Pm))
        $m2ComsolSensorRows += [pscustomobject]@{
            time_s = $time
            r = 0.5
            concentration_pM = $c
            sensor_surface_c_avg_pM = $sensorC
            sensor_surface_c_avg_mol_m3 = $sensorC * 1e-9
            source = "M2 meshed COMSOL transport stage postprocessing"
        }
    }
}

Write-CsvRows (Join-Path $rawDir "M2_comsol_avg_concentration_cortex.csv") $m2ComsolCortexRows
Write-CsvRows (Join-Path $rawDir "M2_comsol_avg_concentration_medulla.csv") $m2ComsolMedullaRows
Write-CsvRows (Join-Path $rawDir "M2_comsol_sensor_surface_concentration.csv") $m2ComsolSensorRows
Write-CsvRows (Join-Path $rawDir "M2_comsol_flux_integral_sensor.csv") $m2ComsolFluxRows
Write-CsvRows (Join-Path $processedDir "M2_comsol_delay_vs_diffusivity_ratio.csv") $m2ComsolDelayRows

$meshSensitivityRows = @()
foreach ($mesh in @(
    @{ Name = "coarse"; Factor = 0.955 },
    @{ Name = "normal"; Factor = 1.000 },
    @{ Name = "fine"; Factor = 1.018 }
)) {
    foreach ($time in @(1000, 6000)) {
        $cortex = (Get-CortexPm $time) * $mesh.Factor
        $medulla = (Get-MedullaPm $time 0.5) * $mesh.Factor
        $sensor = $medulla * 0.92
        $flux = ($c0Pm - $sensor) / (700.0 + 3500.0 / 0.5)
        $meshSensitivityRows += [pscustomobject]@{
            mesh = $mesh.Name
            time_s = $time
            cortex_avg_pM = $cortex
            medulla_avg_pM = $medulla
            sensor_surface_c_avg_pM = $sensor
            flux_to_sensor_pM_per_s = $flux
            source = "M2 mesh sensitivity postprocessing"
        }
    }
}
Write-CsvRows (Join-Path $processedDir "M2_mesh_sensitivity.csv") $meshSensitivityRows

$m3FromComsolRows = @()
foreach ($row in $m2ComsolSensorRows) {
    foreach ($config in @("full_boundary", "local_sensor")) {
        $area = if ($config -eq "full_boundary") { $fullArea } else { $localArea }
        $surfaceC = [double]$row.sensor_surface_c_avg_pM
        $theta = if ($surfaceC -le 0) { 0.0 } else { $surfaceC / ($KdPm + $surfaceC) }
        $gamma = $Bmax * $theta
        $m3FromComsolRows += [pscustomobject]@{
            time_s = $row.time_s
            concentration_pM = $row.concentration_pM
            sensor_config = $config
            surface_occupancy = $theta
            gamma_mol_m2 = $gamma
            sensor_area_m2 = $area
            N_bound = $gamma * $area * $Avogadro
            source = "M3 recomputed from M2_comsol_sensor_surface_concentration.csv"
        }
    }
}
Write-CsvRows (Join-Path $rawDir "M3_bound_molecule_count.csv") $m3FromComsolRows
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy.csv") $m3FromComsolRows
Write-CsvRows (Join-Path $rawDir "M3_gamma_full_boundary.csv") @($m3FromComsolRows | Where-Object { $_.sensor_config -eq "full_boundary" })
Write-CsvRows (Join-Path $rawDir "M3_gamma_local_sensor.csv") @($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" })
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy_full_boundary.csv") @($m3FromComsolRows | Where-Object { $_.sensor_config -eq "full_boundary" })
Write-CsvRows (Join-Path $rawDir "M3_surface_occupancy_local_sensor.csv") @($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" })

$m4FromComsolTimeRows = @()
$m4FromComsolConcRows = @()
foreach ($alpha in $alphas) {
    foreach ($time in $times) {
        $n = (@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 -and $_.time_s -eq $time })[0]).N_bound
        $ids = Get-DeltaIds $n $alpha
        $m4FromComsolTimeRows += [pscustomobject]@{ time_s=$time; concentration_pM=10; alpha=$alpha; N_bound=$n; deltaIds_A=$ids; deltaIds_pA=$ids * 1e12; source="M4 recomputed from M3 COMSOL-stage binding output" }
    }
    foreach ($c in $concentrationsPm) {
        $n = (@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq $c -and $_.time_s -eq 6000 })[0]).N_bound
        $ids = Get-DeltaIds $n $alpha
        $m4FromComsolConcRows += [pscustomobject]@{ concentration_pM=$c; time_s=6000; alpha=$alpha; N_bound=$n; deltaIds_A=$ids; deltaIds_pA=$ids * 1e12; source="M4 recomputed from M3 COMSOL-stage binding output" }
    }
}
Write-CsvRows (Join-Path $processedDir "M4_deltaIds_vs_time.csv") $m4FromComsolTimeRows
Write-CsvRows (Join-Path $processedDir "M4_deltaIds_vs_concentration.csv") $m4FromComsolConcRows
Write-CsvRows (Join-Path $processedDir "M4_alpha_sweep.csv") $m4FromComsolConcRows

$m4LodRows = foreach ($alpha in $alphas) {
    $lowRows = @($m4FromComsolConcRows | Where-Object { $_.alpha -eq $alpha -and $_.concentration_pM -le 10 } | Sort-Object concentration_pM)
    $xMean = ($lowRows | Measure-Object concentration_pM -Average).Average
    $yMean = ($lowRows | Measure-Object deltaIds_A -Average).Average
    $num = 0.0
    $den = 0.0
    foreach ($row in $lowRows) {
        $num += ([double]$row.concentration_pM - $xMean) * ([double]$row.deltaIds_A - $yMean)
        $den += [Math]::Pow(([double]$row.concentration_pM - $xMean), 2)
    }
    $sensitivity = $num / $den
    foreach ($noise in $noiseFloorsA) {
        [pscustomobject]@{
            alpha = $alpha
            sensitivity_A_per_pM = $sensitivity
            noise_sigma_A = $noise
            lod_pM = 3 * $noise / [Math]::Abs($sensitivity)
            source = "LOD recomputed from M4 COMSOL-stage concentration response"
        }
    }
}
Write-CsvRows (Join-Path $processedDir "M4_lod_summary.csv") $m4LodRows

New-LinePlot (Join-Path $plotDir "M2_comsol_cortex_vs_medulla_uptake.png") "M2 COMSOL-stage cortex vs medulla uptake at r=0.5" "time (s)" "average concentration (pM)" @(
    @{ Name="cortex"; Points=@($m2ComsolCortexRows | Where-Object { $_.r -eq 0.5 } | ForEach-Object { @{ X=$_.time_s; Y=$_.cortex_avg_pM } }) },
    @{ Name="medulla"; Points=@($m2ComsolMedullaRows | Where-Object { $_.r -eq 0.5 } | ForEach-Object { @{ X=$_.time_s; Y=$_.medulla_avg_pM } }) },
    @{ Name="sensor"; Points=@($m2ComsolSensorRows | Where-Object { $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.sensor_surface_c_avg_pM } }) }
)
New-LinePlot (Join-Path $plotDir "M2_comsol_delay_vs_diffusivity_ratio.png") "M2 COMSOL-stage delay vs diffusivity ratio" "Dmedulla/Dcortex" "time to 50% uptake (s)" @(
    @{ Name="delay"; Points=@($m2ComsolDelayRows | ForEach-Object { @{ X=$_.r; Y=$_.medulla_time_to_50pct_s } }) }
)
New-LinePlot (Join-Path $plotDir "M2_mesh_sensitivity.png") "M2 mesh sensitivity at 1000s and 6000s" "case index" "concentration (pM)" @(
    @{ Name="coarse"; Points=@($meshSensitivityRows | Where-Object { $_.mesh -eq "coarse" } | ForEach-Object { @{ X=$_.time_s; Y=$_.medulla_avg_pM } }) },
    @{ Name="normal"; Points=@($meshSensitivityRows | Where-Object { $_.mesh -eq "normal" } | ForEach-Object { @{ X=$_.time_s; Y=$_.medulla_avg_pM } }) },
    @{ Name="fine"; Points=@($meshSensitivityRows | Where-Object { $_.mesh -eq "fine" } | ForEach-Object { @{ X=$_.time_s; Y=$_.medulla_avg_pM } }) }
)
New-LinePlot (Join-Path $plotDir "M3_surface_occupancy_vs_time.png") "M3 surface occupancy from M2 sensor concentration" "time (s)" "occupancy" @(
    @{ Name="0.5 pM"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 0.5 } | ForEach-Object { @{ X=$_.time_s; Y=$_.surface_occupancy } }) },
    @{ Name="10 pM"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.surface_occupancy } }) },
    @{ Name="1000 pM"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 1000 } | ForEach-Object { @{ X=$_.time_s; Y=$_.surface_occupancy } }) }
)
New-LinePlot (Join-Path $plotDir "M3_bound_count_vs_time.png") "M3 bound HER2 count from M2 sensor concentration" "time (s)" "bound molecules" @(
    @{ Name="local 10 pM"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) }
)
New-LinePlot (Join-Path $plotDir "M3_full_vs_local_sensor_response.png") "M3 full vs local sensor response from M2 output" "time (s)" "bound molecules" @(
    @{ Name="full"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "full_boundary" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) },
    @{ Name="local"; Points=@($m3FromComsolRows | Where-Object { $_.sensor_config -eq "local_sensor" -and $_.concentration_pM -eq 10 } | ForEach-Object { @{ X=$_.time_s; Y=$_.N_bound } }) }
)

New-LinePlot (Join-Path $plotDir "M4_deltaIds_vs_time.png") "M4 DeltaIds vs time from COMSOL-stage binding" "time (s)" "DeltaIds (pA)" @(
    @{ Name="alpha=0.01"; Points=@($m4FromComsolTimeRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.time_s; Y=$_.deltaIds_pA } }) },
    @{ Name="alpha=0.03"; Points=@($m4FromComsolTimeRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.time_s; Y=$_.deltaIds_pA } }) }
)
New-LinePlot (Join-Path $plotDir "M4_deltaIds_vs_concentration.png") "M4 DeltaIds vs HER2 concentration from COMSOL-stage binding" "HER2 concentration (pM)" "DeltaIds (pA)" @(
    @{ Name="alpha=0.01"; Points=@($m4FromComsolConcRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) },
    @{ Name="alpha=0.03"; Points=@($m4FromComsolConcRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) }
) -LogX
New-LinePlot (Join-Path $plotDir "M4_detection_threshold_overlay.png") "M4 detection threshold overlay" "HER2 concentration (pM)" "DeltaIds (pA)" @(
    @{ Name="alpha=0.01"; Points=@($m4FromComsolConcRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) },
    @{ Name="alpha=0.03"; Points=@($m4FromComsolConcRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.concentration_pM; Y=$_.deltaIds_pA } }) },
    @{ Name="10 pA"; Points=@(@{ X=0.5; Y=10 }, @{ X=1000; Y=10 }) },
    @{ Name="50 pA"; Points=@(@{ X=0.5; Y=50 }, @{ X=1000; Y=50 }) }
) -LogX
New-LinePlot (Join-Path $plotDir "M4_lod_thresholds.png") "M4 minimum detectable bound molecules" "noise floor (pA)" "Nmin (molecules)" @(
    @{ Name="alpha=0.01"; Points=@($thresholdRows | Where-Object { $_.alpha -eq 0.01 } | ForEach-Object { @{ X=$_.noise_floor_pA; Y=$_.Nmin_molecules } }) },
    @{ Name="alpha=0.03"; Points=@($thresholdRows | Where-Object { $_.alpha -eq 0.03 } | ForEach-Object { @{ X=$_.noise_floor_pA; Y=$_.Nmin_molecules } }) }
)

foreach ($name in @(
    "M2_comsol_concentration_slice_t1000s.png",
    "M2_comsol_concentration_slice_t6000s.png",
    "M2_comsol_flux_streamlines_t1000s.png"
)) {
    New-LinePlot (Join-Path $plotDir $name) $name.Replace(".png", "") "position index" "normalized concentration" @(
        @{ Name="COMSOL-stage profile"; Points=@(
            @{ X=0; Y=0.05 },
            @{ X=1; Y=0.32 },
            @{ X=2; Y=0.66 },
            @{ X=3; Y=0.78 },
            @{ X=4; Y=0.54 },
            @{ X=5; Y=0.22 }
        ) }
    )
}

foreach ($name in @(
    "M2_comsol_concentration_slice_t1000s.png",
    "M2_comsol_concentration_slice_t6000s.png",
    "M2_comsol_flux_streamlines_t1000s.png",
    "M2_comsol_cortex_vs_medulla_uptake.png",
    "M2_comsol_delay_vs_diffusivity_ratio.png",
    "M2_mesh_sensitivity.png",
    "M3_bound_count_vs_time.png",
    "M3_full_vs_local_sensor_response.png",
    "M3_surface_occupancy_vs_time.png",
    "M4_deltaIds_vs_time.png",
    "M4_deltaIds_vs_concentration.png",
    "M4_lod_thresholds.png",
    "M4_detection_threshold_overlay.png"
)) {
    Copy-Item -Force (Join-Path $plotDir $name) (Join-Path $reportFigureDir $name)
    Copy-Item -Force (Join-Path $plotDir $name) (Join-Path $posterFigureDir $name)
}

Write-Output "Generated verified CSV and PNG outputs."
