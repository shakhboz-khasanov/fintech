from app.schemas.deposit import DepositRequest, DepositResponse, DepositMatch

# Real deposit catalog from bank.uz (March 2026)
DEPOSIT_CATALOG = [
    # ── UZS deposits ──────────────────────────────────────────────────────────
    {"bank_name": "Uzum Bank",       "bank_slug": "uzum_bank",    "product_name": "Moslashuvchan",         "currency": "uzs", "rate_pct": 24.0, "term_months": 18,  "min_amount_uzs": 10_000,     "early_withdrawal": True,  "notes": "Kunlik hisoblash"},
    {"bank_name": "AVO Bank",        "bank_slug": "avo_bank",     "product_name": "AVO omonat",            "currency": "uzs", "rate_pct": 25.0, "term_months": 6,   "min_amount_uzs": 100_000,    "early_withdrawal": False, "notes": ""},
    {"bank_name": "Agrobank",        "bank_slug": "agrobank",     "product_name": "Katta omonat",          "currency": "uzs", "rate_pct": 23.0, "term_months": 25,  "min_amount_uzs": 50_000_000, "early_withdrawal": False, "notes": "Min 50M UZS"},
    {"bank_name": "O'zsanoat",       "bank_slug": "uzsanoat",     "product_name": "Konstruktor",           "currency": "uzs", "rate_pct": 21.0, "term_months": 24,  "min_amount_uzs": 1_000_000,  "early_withdrawal": False, "notes": ""},
    {"bank_name": "Ipak Yo'li Bank", "bank_slug": "ipak_yoli",    "product_name": "Quyoshli",              "currency": "uzs", "rate_pct": 20.0, "term_months": 24,  "min_amount_uzs": 500_000,    "early_withdrawal": False, "notes": ""},
    {"bank_name": "Agrobank",        "bank_slug": "agrobank",     "product_name": "Progress",              "currency": "uzs", "rate_pct": 21.0, "term_months": 13,  "min_amount_uzs": 1_000_000,  "early_withdrawal": False, "notes": ""},
    {"bank_name": "Kapitalbank",     "bank_slug": "kapitalbank",  "product_name": "Kapital omonat",        "currency": "uzs", "rate_pct": 22.0, "term_months": 24,  "min_amount_uzs": 1_000_000,  "early_withdrawal": False, "notes": ""},
    {"bank_name": "Asakabank",       "bank_slug": "asakabank",    "product_name": "Avans (oldindan foiz)",  "currency": "uzs", "rate_pct": 22.0, "term_months": 18,  "min_amount_uzs": 1_000_000,  "early_withdrawal": False, "notes": "Foiz oldindan to'lanadi"},
    {"bank_name": "Hamkorbank",      "bank_slug": "hamkorbank",   "product_name": "Maqsadli jamg'arma",    "currency": "uzs", "rate_pct": 19.0, "term_months": 18,  "min_amount_uzs": 500_000,    "early_withdrawal": False, "notes": ""},
    {"bank_name": "NBU",             "bank_slug": "nbu",          "product_name": "Hamma uchun",           "currency": "uzs", "rate_pct": 21.0, "term_months": 18,  "min_amount_uzs": 100_000,    "early_withdrawal": True,  "notes": "Onlayn ochish mumkin"},
    {"bank_name": "Ipoteka Bank",    "bank_slug": "ipoteka_bank", "product_name": "Ipoteka jamg'armasi",   "currency": "uzs", "rate_pct": 7.0,  "term_months": 24,  "min_amount_uzs": 1_000_000,  "early_withdrawal": False, "notes": "Ipoteka uchun boshlang'ich to'lov"},
    # ── USD deposits ──────────────────────────────────────────────────────────
    {"bank_name": "Anorbank",        "bank_slug": "anorbank",     "product_name": "ELITE",                 "currency": "usd", "rate_pct": 7.0,  "term_months": 24,  "min_amount_usd": 500_000,    "early_withdrawal": False, "notes": "Min $500,000"},
    {"bank_name": "TBC Bank",        "bank_slug": "tbc_bank",     "product_name": "Muddatli depozit",      "currency": "usd", "rate_pct": 6.5,  "term_months": 24,  "min_amount_usd": 1_000,      "early_withdrawal": False, "notes": ""},
    {"bank_name": "TBC Bank",        "bank_slug": "tbc_bank",     "product_name": "Muddatli depozit",      "currency": "usd", "rate_pct": 5.5,  "term_months": 13,  "min_amount_usd": 1_000,      "early_withdrawal": False, "notes": ""},
    {"bank_name": "Xalq Banki",      "bank_slug": "xalq_banki",   "product_name": "Stimul-2",              "currency": "usd", "rate_pct": 4.5,  "term_months": 18,  "min_amount_usd": 100,        "early_withdrawal": False, "notes": ""},
    {"bank_name": "NBU",             "bank_slug": "nbu",          "product_name": "USD omonat",            "currency": "usd", "rate_pct": 5.0,  "term_months": 18,  "min_amount_usd": 100,        "early_withdrawal": False, "notes": ""},
    {"bank_name": "Ipak Yo'li Bank", "bank_slug": "ipak_yoli",    "product_name": "Bahor tiklanish-8",     "currency": "usd", "rate_pct": 3.0,  "term_months": 6,   "min_amount_usd": 500,        "early_withdrawal": False, "notes": ""},
]

USD_RATE = 12_700  # approximate UZS per 1 USD


def match_deposits(req: DepositRequest) -> DepositResponse:
    amount_uzs = req.amount_uzs or 0
    amount_usd = req.amount_usd or (amount_uzs / USD_RATE if amount_uzs else 0)
    amount_uzs = amount_uzs or (amount_usd * USD_RATE)

    currency = req.preferred_currency.lower()
    term     = req.preferred_term_months

    matches = []
    for d in DEPOSIT_CATALOG:
        cur = d["currency"]

        # Filter by early withdrawal preference
        if req.needs_early_withdrawal and not d.get("early_withdrawal", False):
            continue

        # Check minimum amount
        if cur == "uzs":
            min_amt = d.get("min_amount_uzs", 0)
            if amount_uzs < min_amt:
                continue
            deposit_amount = amount_uzs
        else:
            min_amt = d.get("min_amount_usd", 0)
            if amount_usd < min_amt:
                continue
            deposit_amount = amount_usd

        # Score: base rate + term match bonus + currency preference bonus
        score = d["rate_pct"]
        if term and abs(d["term_months"] - term) <= 3:
            score += 1.0
        if cur == currency:
            score += 0.5

        # Projected return
        projected = deposit_amount * (d["rate_pct"] / 100) * (d["term_months"] / 12)

        matches.append(DepositMatch(
            bank_name=d["bank_name"],
            bank_slug=d["bank_slug"],
            product_name=d["product_name"],
            currency=cur,
            rate_pct=d["rate_pct"],
            term_months=d["term_months"],
            min_amount=min_amt or None,
            projected_return=round(projected, 2),
            notes=d.get("notes", ""),
            score=round(score, 2),
        ))

    matches.sort(key=lambda x: x.score, reverse=True)

    uzs_matches = [m for m in matches if m.currency == "uzs"]
    usd_matches = [m for m in matches if m.currency == "usd"]

    tips = _build_tips(amount_uzs, amount_usd, uzs_matches, usd_matches, req)

    return DepositResponse(
        matches=matches,
        best_uzs=uzs_matches[0] if uzs_matches else None,
        best_usd=usd_matches[0] if usd_matches else None,
        tips=tips,
    )


def _build_tips(amount_uzs, amount_usd, uzs, usd, req) -> list[str]:
    tips = []
    if uzs:
        best_rate = uzs[0].rate_pct
        tips.append(
            f"💰 UZS bo'yicha eng yuqori stavka: {best_rate}% — {uzs[0].bank_name} ({uzs[0].product_name})"
        )
    if usd and amount_usd >= 100:
        tips.append(
            f"💵 USD bo'yicha eng yuqori stavka: {usd[0].rate_pct}% — {usd[0].bank_name} ({usd[0].product_name})"
        )
    if amount_uzs > 0 and amount_uzs < 1_000_000:
        tips.append("ℹ️ Ko'pchilik banklarda minimal depozit miqdori 1,000,000 UZS dan boshlanadi.")
    if req.needs_early_withdrawal:
        tips.append("📋 Muddatidan oldin yechib olish imkoniyati bo'lgan mahsulotlar ko'rsatildi.")
    if not usd and amount_usd >= 100:
        tips.append("💡 USD depozit uchun minimal miqdor talablarini tekshiring.")
    return tips
