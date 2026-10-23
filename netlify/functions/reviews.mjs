// Google recenzije za sekciju "Šta kažu klijenti" — /.netlify/functions/reviews?lang=sr|en
// Ključ je SAMO u Netlify env GOOGLE_PLACES_KEY (nikad u kodu); Place ID u GOOGLE_PLACE_ID.
// Netlify CDN kešira odgovor: 24h kad Google vrati podatke, 10 min kad ne vrati ništa ili pukne,
// pa nove recenzije same dođu na sajt bez ponovne objave.
const DAN = 86400
const KRATKO = 600

export default async (req) => {
  const lang = new URL(req.url).searchParams.get("lang") === "en" ? "en" : "sr"
  const key = process.env.GOOGLE_PLACES_KEY
  const place = process.env.GOOGLE_PLACE_ID
  const prazno = { rating: null, userRatingCount: 0, mapsUri: "", reviews: [] }
  if (!key || !place) return odgovor(prazno, KRATKO)

  try {
    const r = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(place)}?languageCode=${lang}`, {
      headers: { "X-Goog-Api-Key": key, "X-Goog-FieldMask": "rating,userRatingCount,reviews,googleMapsUri" },
      signal: AbortSignal.timeout(8000),
    })
    if (!r.ok) return odgovor(prazno, KRATKO)
    const d = await r.json()
    const reviews = (d.reviews || []).slice(0, 5).map((v) => {
      const t = v.originalText || v.text || {}  // tekst na jeziku na kom je napisan, bez prevoda
      const a = v.authorAttribution || {}
      return {
        author: a.displayName || "",
        authorUrl: a.uri || "",
        photo: a.photoUri || "",
        rating: v.rating || 0,
        text: t.text || "",
        lang: t.languageCode || "",
        time: v.relativePublishTimeDescription || "",
        link: v.googleMapsUri || a.uri || "",
      }
    })
    const body = { rating: d.rating ?? null, userRatingCount: d.userRatingCount || 0, mapsUri: d.googleMapsUri || "", reviews }
    return odgovor(body, reviews.length ? DAN : KRATKO)
  } catch {
    return odgovor(prazno, KRATKO)
  }
}

function odgovor(body, ttl) {
  return new Response(JSON.stringify(body), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=600",
      "netlify-cdn-cache-control": `public, durable, s-maxage=${ttl}, stale-while-revalidate=3600`,
    },
  })
}
