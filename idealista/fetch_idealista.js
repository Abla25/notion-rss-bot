// scripts/fetch_idealista.js
// Legge il database Idealista Notion e scrive public/data-idealista.json

import { writeFile, mkdir, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const NOTION_KEY = process.env.NOTION_API_KEY;
const IDEALISTA_DB_ID = process.env.IDEALISTA_NOTION_DATABASE_ID;

if (!NOTION_KEY || !IDEALISTA_DB_ID) {
  console.error("❌ Missing NOTION_API_KEY or IDEALISTA_NOTION_DATABASE_ID");
  process.exit(1);
}

async function fetchAllIdealistaPages() {
  const results = [];
  let has_more = true;
  let next_cursor = undefined;

  console.log("📡 Fetching Idealista listings from Notion...");

  while (has_more) {
    const body = {
      page_size: 100,
      sorts: [
        {
          property: "last_seen",
          direction: "descending"
        }
      ],
      filter: {
        property: "status",
        select: {
          equals: "active"
        }
      },
      ...(next_cursor ? { start_cursor: next_cursor } : {})
    };

    const r = await fetch(`https://api.notion.com/v1/databases/${IDEALISTA_DB_ID}/query`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${NOTION_KEY}`,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
      },
      body: JSON.stringify(body)
    });

    if (!r.ok) {
      const t = await r.text();
      throw new Error(`Notion API ${r.status}: ${t}`);
    }

    const json = await r.json();
    results.push(...json.results);
    has_more = json.has_more;
    next_cursor = json.next_cursor;
    
    console.log(`📊 Fetched ${results.length} listings so far...`);
  }
  
  console.log(`✅ Total Idealista listings fetched: ${results.length}`);
  return results;
}

// Mappa le proprietà Notion Idealista → struttura frontend
function parseIdealistaPage(page) {
  const props = page.properties || {};

  const get = (p, type, path) => {
    try {
      if (type === "title") return props[p]?.title?.[0]?.text?.content || "";
      if (type === "rich") return props[p]?.rich_text?.[0]?.text?.content || "";
      if (type === "number") return props[p]?.number ?? null;
      if (type === "date") return props[p]?.date?.start || "";
      if (type === "url") return props[p]?.url || "";
      if (type === "select") return props[p]?.select?.name || "";
      if (type === "checkbox") return props[p]?.checkbox || false;
      return "";
    } catch {
      return "";
    }
  };

  return {
    id: page.id,
    propertyCode: get("property_code", "rich"),
    title: get("title", "title"),
    description: get("description", "rich"),
    price: get("price", "number"),
    rooms: get("rooms", "number"),
    bathrooms: get("bathrooms", "number"),
    size: get("size", "number"),
    address: get("address", "rich"),
    district: get("district", "select"),
    neighborhood: get("neighborhood", "rich"),
    municipality: get("municipality", "rich"),
    province: get("province", "rich"),
    latitude: get("latitude", "number"),
    longitude: get("longitude", "number"),
    url: get("url", "url"),
    thumbnail: get("thumbnail", "url"),
    status: get("status", "select"),
    newDevelopment: get("new_development", "checkbox"),
    publicationDate: get("publication_date", "date"),
    lastSeen: get("last_seen", "date"),
    source: "Idealista"
  };
}

async function main() {
  console.log("🏠 Starting Idealista data export...");
  
  const raw = await fetchAllIdealistaPages();
  const mapped = raw.map(parseIdealistaPage);
  
  // Filtra solo quelli con dati validi
  const validListings = mapped.filter(listing => 
    listing.title && listing.propertyCode && listing.price
  );
  
  console.log(`📊 Valid listings: ${validListings.length}/${mapped.length}`);

  const outDir = path.join(process.cwd(), "public");
  if (!existsSync(outDir)) await mkdir(outDir, { recursive: true });

  const outPath = path.join(outDir, "data-idealista.json");
  const payload = {
    generatedAt: new Date().toISOString(),
    count: validListings.length,
    totalCount: mapped.length,
    results: validListings
  };

  await writeFile(outPath, JSON.stringify(payload, null, 2), "utf-8");
  console.log(`✅ Written ${outPath} with ${validListings.length} valid listings`);
  
  // Statistiche
  const avgPrice = validListings.reduce((sum, l) => sum + (l.price || 0), 0) / validListings.length;
  const districts = [...new Set(validListings.map(l => l.district).filter(Boolean))];
  
  console.log(`📈 Statistics:`);
  console.log(`   💰 Average price: €${Math.round(avgPrice)}`);
  console.log(`   🏘️ Districts: ${districts.join(", ")}`);
  console.log(`   📅 Last updated: ${new Date().toLocaleString()}`);
}

main().catch((e) => {
  console.error("❌ Error:", e);
  process.exit(1);
});
