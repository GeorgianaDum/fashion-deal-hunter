# Fashion Deal Hunter — MVP public

Dashboard responsive în română, cu acces public, fără cont și fără produse fictive. Funcționează static pe GitHub Pages. **Nu caută încă automat în magazine.** Catalogul partajat pornește gol.

## Publicare gratuită

1. Creează un repository GitHub public, de exemplu `fashion-deal-hunter`.
2. Încarcă toate fișierele acestui director, inclusiv `.github/workflows/pages.yml`.
3. În repository mergi la **Settings → Pages → Build and deployment** și selectează **GitHub Actions**.
4. Workflow-ul `Publică Fashion Deal Hunter` publică site-ul după un push pe ramura `main`.
5. Deschide URL-ul afișat la Settings → Pages; de obicei `https://UTILIZATOR.github.io/fashion-deal-hunter/`. Nu presupune că adresa este deja activă.
6. Pe telefon, deschide linkul și folosește opțiunea browserului „Adaugă pe ecranul principal”.

## Catalog real, fără date inventate

`data/products.json` este catalogul comun tuturor utilizatorilor. Pentru fiecare produs se folosește formatul:

```json
{
  "products": [
    {
      "name": "DENUMIRE REALĂ",
      "brand": "BRAND REAL",
      "store": "Zalando",
      "category": "Sacouri",
      "color": "negru",
      "sizes": ["S", "M"],
      "price_ron": 59.99,
      "old_price_ron": 129.99,
      "url": "https://www.zalando.ro/URL-REAL-AL-PRODUSULUI",
      "image_url": "",
      "checked_at": "2026-10-28T20:00:00+02:00"
    }
  ]
}
```

Exemplul de mai sus explică **doar schema**: NU îl adăuga în catalog fără verificarea produsului, prețului și a stocului. Prețurile trebuie să fie în RON. Nu completa `old_price_ron` decât dacă prețul anterior este afișat de magazin. Pentru un produs fără reducere, folosește `old_price_ron: 0`. `checked_at` trebuie să fie data reală a verificării. `sizes` trebuie să reflecte mărimile confirmate disponibile. Linkul produsului trebuie să fie pe domeniul magazinului din listă.

## Surse și actualizare

Magazine configurate: ABOUT YOU, ePantofi, Zalando, Fashion Days, ASOS, Mango Outlet. Aplicația nu pretinde că are conectoare active pentru acestea. Un colector ulterior va actualiza `data/products.json` doar cu produse reale, în condițiile permise de fiecare magazin. Nu publica automat date extrase neverificate. GitHub Pages nu execută scraping sau cod backend.

## Limite importante

- Căutarea se face doar în catalogul comun existent, nu live pe web.
- Nu există alerte, istoric de preț sau colectare programată în această versiune.
- Linkul public permite oricui să consulte catalogul, nu să îl modifice.
- Nu se garantează gratuitate nelimitată; se aplică limitele și regulile furnizorului de hosting.
- Verifică prețul final și disponibilitatea pe site-ul magazinului înainte de cumpărare.
