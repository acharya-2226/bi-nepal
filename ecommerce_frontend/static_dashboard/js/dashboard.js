(function () {
    const PERIOD_BUCKETS = {
        monthly: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        quarterly: ["Q1", "Q2", "Q3", "Q4"],
        semiannual: ["H1", "H2"],
        annual: ["Year"],
    };

    const ENDPOINTS = [
        { key: "profitability", path: "/analysis/profitability" },
        { key: "discounts", path: "/analysis/discounts" },
        { key: "inventory", path: "/analysis/inventory" },
        { key: "products", path: "/analysis/products" },
        { key: "expenses", path: "/analysis/expenses" },
        { key: "monthly_growth", path: "/analysis/monthly-growth" },
        { key: "breakeven", path: "/analysis/breakeven" },
        { key: "cashflow", path: "/analysis/cashflow" },
    ];

    const state = {
        apiBase: localStorage.getItem("dashboard_api_base") || "http://127.0.0.1:8002",
        period: "monthly",
        bucket: "all",
        payload: {},
        errors: [],
        charts: null,
    };

    function qs(id) {
        return document.getElementById(id);
    }

    function safeNumber(value) {
        const n = Number(value);
        return Number.isFinite(n) ? n : 0;
    }

    function asCurrency(value) {
        if (value === null || value === undefined || value === "") {
            return "N/A";
        }
        return "NPR " + safeNumber(value).toLocaleString(undefined, { maximumFractionDigits: 2 });
    }

    function asPercent(value) {
        if (value === null || value === undefined || value === "") {
            return "N/A";
        }
        return safeNumber(value).toFixed(2) + "%";
    }

    function asText(value) {
        if (value === null || value === undefined || value === "") {
            return "N/A";
        }
        return String(value);
    }

    function setText(id, text) {
        const el = qs(id);
        if (el) {
            el.textContent = text;
        }
    }

    function urlFor(path) {
        const base = state.apiBase.replace(/\/$/, "");
        const url = new URL(base + path);
        url.searchParams.set("period", state.period);
        if (state.bucket && state.bucket !== "all") {
            url.searchParams.set("bucket", state.bucket);
        }
        return url.toString();
    }

    async function fetchEndpoint(endpoint) {
        const response = await fetch(urlFor(endpoint.path));
        if (!response.ok) {
            throw new Error(endpoint.path + " returned " + response.status);
        }
        return response.json();
    }

    async function fetchPayload() {
        const result = {};
        const errors = [];

        await Promise.all(ENDPOINTS.map(async function (endpoint) {
            try {
                result[endpoint.key] = await fetchEndpoint(endpoint);
            } catch (err) {
                result[endpoint.key] = {};
                errors.push(endpoint.path + ": " + (err && err.message ? err.message : String(err)));
            }
        }));

        state.payload = result;
        state.errors = errors;
    }

    function renderErrorPanel() {
        const panel = qs("errorPanel");
        const list = qs("errorList");
        if (!panel || !list) {
            return;
        }

        list.innerHTML = "";
        if (!state.errors.length) {
            panel.hidden = true;
            return;
        }

        state.errors.forEach(function (error) {
            const li = document.createElement("li");
            li.textContent = error;
            list.appendChild(li);
        });
        panel.hidden = false;
    }

    function updateBucketOptions() {
        const select = qs("bucketSelect");
        if (!select) {
            return;
        }

        const buckets = PERIOD_BUCKETS[state.period] || [];
        select.innerHTML = "";

        const allOption = document.createElement("option");
        allOption.value = "all";
        allOption.textContent = "All " + state.period.charAt(0).toUpperCase() + state.period.slice(1);
        select.appendChild(allOption);

        buckets.forEach(function (bucket) {
            const option = document.createElement("option");
            option.value = bucket;
            option.textContent = bucket;
            select.appendChild(option);
        });

        if (state.bucket !== "all" && buckets.indexOf(state.bucket) === -1) {
            state.bucket = "all";
        }
        select.value = state.bucket;
    }

    function updateScopeText() {
        const scopeText = qs("activeScopeText");
        if (!scopeText) {
            return;
        }

        let html = "Active Scope: <strong>" + state.period.charAt(0).toUpperCase() + state.period.slice(1) + "</strong>";
        if (state.bucket !== "all") {
            html += " / <strong>" + state.bucket + "</strong>";
        }
        scopeText.innerHTML = html;

        const titlePeriod = state.period.charAt(0).toUpperCase() + state.period.slice(1);
        setText("growthTitle", titlePeriod + " Revenue vs Profit");
        setText("cashflowTitle", titlePeriod + " Cashflow");
    }

    function renderKpis() {
        const profitability = state.payload.profitability || {};
        const cashflow = state.payload.cashflow || {};
        const inventory = state.payload.inventory || {};

        setText("kpiNetRevenue", asCurrency(profitability.net_revenue_npr));
        setText("kpiNetProfit", asCurrency(profitability.net_profit_npr));
        setText("kpiNetProfitMargin", asPercent(profitability.net_profit_margin_pct));
        setText("kpiCashMovement", asCurrency(cashflow.net_cash_movement_npr));
        setText("kpiInventoryTurnover", asText(inventory.inventory_turnover) + (inventory.inventory_turnover ? "x" : ""));
        setText("kpiReorderAlerts", asText(inventory.items_below_reorder_level));
    }

    function normalizedGrowthRows() {
        const monthly = (((state.payload.monthly_growth || {}).monthly) || []);
        return monthly.map(function (row, idx) {
            return {
                label: row.PeriodLabel || row.MonthName || String(idx + 1),
                revenue: safeNumber(row.MonthRevenue),
                profit: safeNumber(row.MonthProfit),
            };
        });
    }

    function normalizedCashRows() {
        const rows = (((state.payload.cashflow || {}).monthly_cashflow) || []);
        return rows.map(function (row, idx) {
            return {
                label: row.PeriodLabel || String(row.MonthNum || idx + 1),
                cashIn: safeNumber(row.CashIn),
                cashOut: safeNumber(row.CashOut),
                netCash: safeNumber(row.NetCash),
            };
        });
    }

    function renderPeriodKpis(growthRows, cashRows) {
        if (!growthRows.length || !cashRows.length) {
            setText("periodRevenue", "N/A");
            setText("periodProfit", "N/A");
            setText("periodMargin", "N/A");
            setText("periodNetCash", "N/A");
            return;
        }

        const revenue = growthRows.reduce(function (sum, r) { return sum + r.revenue; }, 0);
        const profit = growthRows.reduce(function (sum, r) { return sum + r.profit; }, 0);
        const netCash = cashRows.reduce(function (sum, r) { return sum + r.netCash; }, 0);
        const margin = revenue > 0 ? (profit / revenue) * 100 : 0;

        setText("periodRevenue", asCurrency(revenue));
        setText("periodProfit", asCurrency(profit));
        setText("periodMargin", margin.toFixed(2) + "%");
        setText("periodNetCash", asCurrency(netCash));
    }

    function ensureCharts() {
        if (state.charts || typeof ApexCharts !== "function") {
            return;
        }

        const growthChart = new ApexCharts(document.querySelector("#growthChart"), {
            chart: { type: "line", height: 320, toolbar: { show: false } },
            series: [
                { name: "Revenue", data: [] },
                { name: "Profit", data: [] },
            ],
            noData: { text: "No growth data available" },
            xaxis: { categories: [] },
            stroke: { width: [3, 3], curve: "smooth" },
            colors: ["#0A9396", "#CA6702"],
            legend: { position: "top" },
        });

        const cashflowChart = new ApexCharts(document.querySelector("#cashflowChart"), {
            chart: { type: "bar", height: 320, toolbar: { show: false } },
            series: [
                { name: "Cash In", data: [] },
                { name: "Cash Out", data: [] },
                { name: "Net Cash", data: [] },
            ],
            noData: { text: "No cashflow data available" },
            xaxis: { categories: [] },
            colors: ["#005F73", "#BB3E03", "#94D2BD"],
            plotOptions: { bar: { borderRadius: 4, columnWidth: "45%" } },
            legend: { position: "top" },
        });

        const expenseChart = new ApexCharts(document.querySelector("#expenseChart"), {
            chart: { type: "donut", height: 320 },
            labels: [],
            series: [],
            noData: { text: "No expense data available" },
            colors: ["#005F73", "#0A9396", "#94D2BD", "#EE9B00", "#CA6702", "#BB3E03", "#AE2012"],
            legend: { position: "bottom" },
        });

        growthChart.render();
        cashflowChart.render();
        expenseChart.render();

        state.charts = { growthChart: growthChart, cashflowChart: cashflowChart, expenseChart: expenseChart };
    }

    function renderCharts() {
        ensureCharts();
        if (!state.charts) {
            return;
        }

        const growthRows = normalizedGrowthRows();
        const cashRows = normalizedCashRows();

        state.charts.growthChart.updateOptions({
            xaxis: { categories: growthRows.map(function (row) { return row.label; }) },
        });
        state.charts.growthChart.updateSeries([
            { name: "Revenue", data: growthRows.map(function (row) { return row.revenue; }) },
            { name: "Profit", data: growthRows.map(function (row) { return row.profit; }) },
        ]);

        state.charts.cashflowChart.updateOptions({
            xaxis: { categories: cashRows.map(function (row) { return row.label; }) },
        });
        state.charts.cashflowChart.updateSeries([
            { name: "Cash In", data: cashRows.map(function (row) { return row.cashIn; }) },
            { name: "Cash Out", data: cashRows.map(function (row) { return row.cashOut; }) },
            { name: "Net Cash", data: cashRows.map(function (row) { return row.netCash; }) },
        ]);

        const breakdown = ((state.payload.expenses || {}).expense_breakdown) || {};
        const labels = Object.keys(breakdown);
        const series = labels.map(function (label) { return safeNumber(breakdown[label]); });
        state.charts.expenseChart.updateOptions({ labels: labels });
        state.charts.expenseChart.updateSeries(series);

        renderPeriodKpis(growthRows, cashRows);
        renderBucketList(growthRows);
    }

    function renderBucketList(growthRows) {
        const list = qs("periodBucketList");
        if (!list) {
            return;
        }

        list.innerHTML = "";
        if (!growthRows.length) {
            const li = document.createElement("li");
            li.textContent = "No period buckets available.";
            list.appendChild(li);
            return;
        }

        growthRows.forEach(function (row) {
            const li = document.createElement("li");
            li.textContent = row.label;
            list.appendChild(li);
        });
    }

    function createStatsRow(label, value) {
        const row = document.createElement("div");
        const span = document.createElement("span");
        span.textContent = label;
        const strong = document.createElement("strong");
        strong.textContent = value;
        row.appendChild(span);
        row.appendChild(strong);
        return row;
    }

    function renderStatsPanels() {
        const profitability = state.payload.profitability || {};
        const expenses = state.payload.expenses || {};
        const breakeven = state.payload.breakeven || {};
        const discounts = state.payload.discounts || {};

        const profitabilityList = qs("profitabilityList");
        if (profitabilityList) {
            profitabilityList.innerHTML = "";
            const title = document.createElement("h2");
            title.textContent = "Profitability Snapshot";
            profitabilityList.appendChild(title);

            profitabilityList.appendChild(createStatsRow("Gross Revenue", asCurrency(profitability.gross_revenue_npr)));
            profitabilityList.appendChild(createStatsRow("Total Discount", asCurrency(profitability.total_discount_npr)));
            profitabilityList.appendChild(createStatsRow("COGS", asCurrency(profitability.cogs_npr)));
            profitabilityList.appendChild(createStatsRow("Gross Profit Margin", asPercent(profitability.gross_profit_margin_pct)));
            profitabilityList.appendChild(createStatsRow("Operating Expense Ratio", asPercent(expenses.opex_pct_of_revenue)));
            profitabilityList.appendChild(createStatsRow("Weighted Avg Cost", asCurrency(breakeven.weighted_avg_cost_npr)));
            profitabilityList.appendChild(createStatsRow("Avg Contrib / Unit", asCurrency(breakeven.avg_contrib_per_unit_npr)));
            profitabilityList.appendChild(createStatsRow("Actual Units Sold", asText(breakeven.actual_units_sold)));
            profitabilityList.appendChild(createStatsRow("Margin of Safety", asPercent(breakeven.margin_of_safety_pct)));
        }

        const discountList = qs("discountList");
        if (discountList) {
            discountList.innerHTML = "";
            const title = document.createElement("h2");
            title.textContent = "Discount Insights";
            discountList.appendChild(title);

            discountList.appendChild(createStatsRow("Discount % of Revenue", asPercent(discounts.discount_pct_of_revenue)));
            discountList.appendChild(createStatsRow("Discounted Transactions", asText(discounts.discounted_transactions)));
            discountList.appendChild(createStatsRow("Total Transactions", asText(discounts.total_transactions)));
            discountList.appendChild(createStatsRow("Discounted Txn %", asPercent(discounts.discounted_txn_pct)));
            discountList.appendChild(createStatsRow("Avg Discount / Txn", asCurrency(discounts.avg_discount_per_txn_npr)));
        }
    }

    function renderTable(bodyId, rows, columns, emptyMessage) {
        const body = qs(bodyId);
        if (!body) {
            return;
        }

        body.innerHTML = "";
        if (!rows.length) {
            const tr = document.createElement("tr");
            const td = document.createElement("td");
            td.colSpan = columns.length;
            td.textContent = emptyMessage;
            tr.appendChild(td);
            body.appendChild(tr);
            return;
        }

        rows.forEach(function (row) {
            const tr = document.createElement("tr");
            columns.forEach(function (column) {
                const td = document.createElement("td");
                td.textContent = row[column] === undefined || row[column] === null ? "N/A" : String(row[column]);
                tr.appendChild(td);
            });
            body.appendChild(tr);
        });
    }

    function renderTables() {
        const discounts = state.payload.discounts || {};
        const products = state.payload.products || {};
        const expenses = state.payload.expenses || {};
        const inventory = state.payload.inventory || {};
        const breakeven = state.payload.breakeven || {};

        renderTable(
            "discountTableBody",
            discounts.monthly_discount || [],
            ["MonthNum", "monthly_discount_npr"],
            "No discount rows available for this scope."
        );

        renderTable(
            "productsTableBody",
            products.top_10_products_by_revenue || [],
            ["ItemID", "ItemName", "Category", "ProductQtySold", "ProductRevenue", "ProductProfit", "ContribPct"],
            "No product rows available."
        );

        renderTable(
            "categoryRevenueBody",
            products.revenue_by_category || [],
            ["Category", "category_revenue_npr"],
            "No category revenue rows available."
        );

        renderTable(
            "monthlyExpenseBody",
            expenses.monthly_expenses || [],
            ["Month", "TotalExpense"],
            "No expense rows available for this scope."
        );

        renderTable(
            "reorderBody",
            inventory.below_reorder_items || [],
            ["ItemID", "ItemName", "ClosingStock", "ReorderLevel"],
            "No items currently below reorder level."
        );

        renderTable(
            "breakevenBody",
            breakeven.top_20_easiest_breakeven || [],
            ["ItemID", "ItemName", "BreakEvenUnits", "ContribPerUnit"],
            "No break-even rows available."
        );
    }

    function renderReportLinks() {
        const pdf = qs("pdfReportLink");
        const excel = qs("excelReportLink");
        if (pdf) {
            pdf.href = urlFor("/report/pdf");
        }
        if (excel) {
            excel.href = urlFor("/report/excel");
        }
    }

    function renderBackendInspector() {
        const endpointSelect = qs("endpointSelect");
        const endpointJson = qs("endpointJson");
        const errorJson = qs("errorJson");

        if (!endpointSelect || !endpointJson || !errorJson) {
            return;
        }

        const keys = Object.keys(state.payload).sort();
        endpointSelect.innerHTML = "";

        keys.forEach(function (key) {
            const option = document.createElement("option");
            option.value = key;
            option.textContent = key;
            endpointSelect.appendChild(option);
        });

        function paint() {
            if (!keys.length) {
                endpointJson.textContent = "{}";
                return;
            }
            const selected = endpointSelect.value || keys[0];
            endpointJson.textContent = JSON.stringify(state.payload[selected], null, 2);
        }

        endpointSelect.onchange = paint;
        paint();
        errorJson.textContent = JSON.stringify(state.errors, null, 2);
    }

    function enableTableFilter(inputId, tableId) {
        const input = qs(inputId);
        const table = qs(tableId);
        if (!input || !table) {
            return;
        }

        input.addEventListener("input", function () {
            const query = input.value.trim().toLowerCase();
            const rows = Array.from(table.querySelectorAll("tbody tr"));
            rows.forEach(function (row) {
                const rowText = row.textContent.toLowerCase();
                row.style.display = rowText.indexOf(query) === -1 ? "none" : "";
            });
        });
    }

    function enableSectionSpy() {
        const navLinks = Array.from(document.querySelectorAll(".side-nav a"));
        const sections = navLinks
            .map(function (link) {
                return document.querySelector(link.getAttribute("href"));
            })
            .filter(Boolean);

        navLinks.forEach(function (link) {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                const target = document.querySelector(link.getAttribute("href"));
                if (target) {
                    target.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            });
        });

        if (!sections.length || typeof IntersectionObserver !== "function") {
            return;
        }

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) {
                    return;
                }

                const id = entry.target.getAttribute("id");
                navLinks.forEach(function (link) {
                    const active = link.getAttribute("href") === "#" + id;
                    link.classList.toggle("active", active);
                });
            });
        }, {
            rootMargin: "-20% 0px -65% 0px",
            threshold: [0.1, 0.4, 0.7],
        });

        sections.forEach(function (section) {
            observer.observe(section);
        });
    }

    async function loadDashboard() {
        updateBucketOptions();
        updateScopeText();
        renderReportLinks();

        await fetchPayload();
        renderErrorPanel();
        renderKpis();
        renderCharts();
        renderStatsPanels();
        renderTables();
        renderBackendInspector();
    }

    function bindForm() {
        const form = qs("scopeForm");
        const apiBaseInput = qs("apiBaseInput");
        const periodSelect = qs("periodSelect");
        const bucketSelect = qs("bucketSelect");

        if (!form || !apiBaseInput || !periodSelect || !bucketSelect) {
            return;
        }

        apiBaseInput.value = state.apiBase;
        periodSelect.value = state.period;

        periodSelect.addEventListener("change", function () {
            state.period = periodSelect.value;
            state.bucket = "all";
            updateBucketOptions();
        });

        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            state.apiBase = apiBaseInput.value.trim() || "http://127.0.0.1:8002";
            state.period = periodSelect.value;
            state.bucket = bucketSelect.value || "all";
            localStorage.setItem("dashboard_api_base", state.apiBase);
            await loadDashboard();
        });
    }

    enableTableFilter("productsFilter", "productsTable");
    enableTableFilter("reorderFilter", "reorderTable");
    enableTableFilter("breakevenFilter", "breakevenTable");
    enableSectionSpy();
    bindForm();

    loadDashboard();
})();
