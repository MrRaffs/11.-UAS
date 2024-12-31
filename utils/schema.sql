-- Tabungan
CREATE TABLE "tabungan" (
	"id"	INTEGER,
	"kategori"	TEXT NOT NULL UNIQUE,
	"saldo"	NUMERIC,
    "updated_at"	TEXT,

	PRIMARY KEY("id" AUTOINCREMENT)
);

-- 