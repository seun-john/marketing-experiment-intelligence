# Public project page verification

31 October 2026: Chrome verified conversion, visit and spending selections against aggregate results; dashboard image selection updated correctly. At a 390px viewport, document width was 375px (vertical scrollbar accounted for), with no horizontal overflow or missing images. The desktop and mobile layouts were visually inspected. Three additional pytest checks passed: original-record reconciliation of public aggregates, local-link resolution and byte equality of report/CSV downloads. See public_page_tests.txt.

The page contains only aggregate data. It explicitly distinguishes the static results explorer from the separately runnable Python/Streamlit application. The page requires no account, paid API, cookies or external JavaScript library. GitHub Pages source: main:/docs. Live publication is verified separately after deployment.
