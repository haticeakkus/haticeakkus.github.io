<?php
	// Initialize variables to hold form data and currency values
	$result = "";
	$amount = "";

	$currency_from = "";
	$currency_to = "";
?>

<!DOCTYPE html>
<html lang="en">

<head>
	<title>Java Jam Coffee House</title>
	<meta name="description" content="CENG 311 Inclass Activity 1" />
</head>

<body>

	<?php
	// Check if the form is submitted
	if (isset($_GET['value']) && isset($_GET['from_currency']) && isset($_GET['to_currency'])) {
		// take the input values
		$amount = floatval($_GET['value']); // convert the input to float
		$currency_from = $_GET['from_currency'];
		$currency_to = $_GET['to_currency'];

		// Define the conversion rates
		$usd_to_cad = 1.35;
		$usd_to_eur = 0.92;
		$cad_to_usd = 0.74;
		$cad_to_eur = 0.68;
		$eur_to_usd = 1.09;
		$eur_to_cad = 1.47;

		// Initialize the result
		$result = 0;

		// Perform the conversion
		switch ($currency_from) {
			case 'FUSD':
				switch ($currency_to) {
					case 'TUSD':
						$result = $amount;
						break;
					case 'TCAD':
						$result = $amount * $usd_to_cad;
						break;
					case 'TEUR':
						$result = $amount * $usd_to_eur;
						break;
				}
				break;
			case 'FCAD':
				switch ($currency_to) {
					case 'TUSD':
						$result = $amount * $cad_to_usd;
						break;
					case 'TCAD':
						$result = $amount;
						break;
					case 'TEUR':
						$result = $amount * $cad_to_eur;
						break;
				}
				break;
			case 'FEUR':
				switch ($currency_to) {
					case 'TUSD':
						$result = $amount * $eur_to_usd;
						break;
					case 'TCAD':
						$result = $amount * $eur_to_cad;
						break;
					case 'TEUR':
						$result = $amount;
						break;
				}
				break;
		}
	}
	?>

	<form action="" method="GET">
		<table>
			<tr>
				<td>
					From:
				</td>
				<td>
					<input type="text" id="input" name="value" value="<?php echo $amount; ?>" />
				</td>
				<td>
					Currency:
				</td>
				<td>
					<!-- Specifies the currency to convert from and retains the user's selection -->
					<select name="from_currency">
						<option value="FUSD" <?php if ($currency_from === 'FUSD') echo 'selected'; ?>>USD</option>
						<option value="FCAD" <?php if ($currency_from === 'FCAD') echo 'selected'; ?>>CAD</option>
						<option value="FEUR" <?php if ($currency_from === 'FEUR') echo 'selected'; ?>>EUR</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>
					To:
				</td>
				<td>
					<input type="text" id="result" name="result" value="<?php echo $result; ?>" readonly />
				</td>
				<td>
					Currency:
				</td>
				<td>
					<!-- Specifies the currency to convert to and retains the user's selection -->
					<select name="to_currency">
						<option value="TUSD" <?php if ($currency_to === 'TUSD') echo 'selected'; ?>>USD</option>
						<option value="TCAD" <?php if ($currency_to === 'TCAD') echo 'selected'; ?>>CAD</option>
						<option value="TEUR" <?php if ($currency_to === 'TEUR') echo 'selected'; ?>>EUR</option>
					</select>
				</td>
			</tr>
			<tr>
				<td>

				</td>
				<td>

				</td>
				<td>

				</td>
				<td>
					<input type="submit" value="convert" />
				</td>
			</tr>
		</table>

	</form>

</body>

</html>