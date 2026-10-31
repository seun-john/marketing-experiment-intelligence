# Data rights and provenance

Original publisher: Kevin Hillstrom / MineThatData, 20 March 2008. The challenge invites public analysis. No explicit licence authorising redistribution of the original customer-level CSV was identified on the publisher page or TensorFlow Datasets catalogue checked 31 October 2026. A website's documentation or code licence does not automatically cover underlying data.

Raw CSV, analytical database and any processed customer-level files are excluded by .gitignore. The acquisition function downloads from the publisher for local analysis and validates before writing. Users must review applicable terms before hosting data or publishing derived artifacts; redistribution clearance remains unresolved. No raw dataset is bundled in the tracked project. Aggregate analytical results are kept with transparent source attribution, without making a blanket licence claim.

The immutable original CSV is hashed in provenance.json. Expected source structure: 64,000 rows, 12 columns, original three assignment strings. Pipeline validates domain coding, missingness, outcome consistency and nonnegative values. No duplicate-looking records are discarded.

Acquisition on 31 October 2026 used the publisher's original HTTP endpoint because its HTTPS certificate failed both Python and Windows validation. TLS verification was not disabled. The source-byte SHA-256 provides reproducibility, not proof of publisher authenticity over unencrypted transport. Validate provenance before relying on this file in a regulated setting.
