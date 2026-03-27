# Notion Bible Import

## Resources

The source files bibles included in this project were downloaded from the web. Each project includes additional resources that are helpful but not a part of this repository.

- [Bible Super Search](https://www.biblesupersearch.com/bible-downloads/)
- [Open Bible](https://openbible.com/)
- [http://labs.bible.org](http://labs.bible.org)

## Source Data

### `bibles_json_6`

Export of all bible versions from [Bible Super Search](https://www.biblesupersearch.com/bible-downloads/) as `.json` files. This includes all languages.

### `bibles_sqlite_6`

Export of all bible versions from [Bible Super Search](https://www.biblesupersearch.com/bible-downloads/) as `.sqlite` files. This includes all languages.

## EN-English/

Export of all **English** bible versions from [Bible Super Search](https://www.biblesupersearch.com/bible-downloads/) as `.csv` files. Note that these are the same versions as the `EN-English` subfolders in `bibles_json_6` and `bibles_sqlite_6`, but in `.csv`.

## Other

- [14-in-1-bibles.xlsx](./14-in-1-bibles.xlsx): Excel file with 14 bible versions in one sheet. Downloaded from [Open Bible](https://openbible.com/). It contains:
  - Verse
  - BSB *(e.g., the translation)*
  - KJV  *(e.g., the translation)*
  - ASV  *(e.g., the translation)*
  - AKJV  *(e.g., the translation)*
  - CPDV  *(e.g., the translation)*
  - DBT  *(e.g., the translation)*
  - DRB  *(e.g., the translation)*
  - ERV  *(e.g., the translation)*
  - JPS / WEY  *(e.g., the translation)*
  - NHEB  *(e.g., the translation)*
  - SLT  *(e.g., the translation)*
  - WBT  *(e.g., the translation)*
  - WEB  *(e.g., the translation)*
  - YLT  *(e.g., the translation)*
- [Bible Books.json](./Bibles//Bible%20Books.json): List of all bible books with their canonical order, chronological order, name, and number of chapters.
- [Bible Chapters (excel).xlsx](./Bibles/Bible%20Chapters%20(excel).xlsx): List of the bible books with their canonical order, testament, short name, full name, # chapters per book, and # verses per chapter
  - *This is a WIP file that was used with the notion import. Only the second page is relevant. The organization is a bit funky but could used manually*
- [bible_languages.csv](./Bibles/bible_languages.csv): Perhaps, a collection of all bible verses in an interlinear format? Very hard to parse manually
  - Includes strongs, greek, etc.
- [bible_translations.xlsx](./Bibles/bible_translations.xlsx)
  - *This appears to be a duplicate of the "14-in-1-bibles.xlsx" file*
- [Bibles.xlsx](./Bibles/Bibles.xlsx): Excel file consolidating the esv and niv translations. It has 3 pages:
  - A list of each book with their canonical order, chronological order, name, and # of chapters
  - A list of each verse an ID (numerical), book, chapter, verse, reference, text (ESV), and footnote / cross-reference
  - A list of each verse an ID (numerical), book, chapter, verse, reference, and text (NIV).
    - *The text appears to include each periscope section*
- [bibleverse.xlsx](./Bibles/bibleverse.xlsx): An .xlsx file with each bible's book, chapter, and number of verses in that chapter. It also includes the number of chapters per book in a separate field.
  - *It contains a web service operator to pull a given verse from the [http://labs.bible.org](http://labs.bible.org) API*
  - > [!IMPORTANT] This pulls the NET version which I don't believe we have anywhere else.
- [books-json.csv](./Bibles//books-json.csv): CSV version of the "Bible Books.json"
  - *Likely easier to just use the .json file*
- [books-notion.csv](./Bibles/books-notion.csv): Basic CSV file with a books ID (numerical), canonical order, name, and # chapters.
- [ESV Bible.csv](./Bibles/ESV%20Bible.csv): .csv file used to import the ESV bible into notion. It includes columns for a random ID (numerical), reference, book, chapter, verse, text, and canonical order.
  - *I believe this is an EXPORT from notion actually.*
- [ESV Bible.json](./Bibles/ESV%20Bible.json): .json file of the ESV bible. It includes a "pk (numerical ID?), translation, book, chapter, verse, text, and footnote/cross-reference.
- [esv-json.csv](./Bibles/esv-json.csv): CSV version of the "ESV Bible.json"
  - *Likely easier to just use the .json file*
- [esv-notion.csv](./Bibles/esv-notion.csv): Separate version of "ESV Bible.csv"?
  - *The columns are slightly different but they contain identical data*
- [kjv_apocrypha_utf8_FINAL.xls](./Bibles/kjv_apocrypha_utf8_FINAL.xls): Simple excel file containing the KJV bible. Includes an ID like this "kjv01Oz1z1" that seems to map the testament, book, verse, etc.
  - *Includes the apocrypha. Should see if other books do the same!*
- [NIV Bible.json](./Bibles/NIV%20Bible.json): .json file of the NIV bible. It includes a "pk (numerical ID?), translation, book, chapter, verse, and text. The format is identical to "ESV Bible.json"
  - *The text tends to include the heading of each periscope?*
- [niv-json.csv](./Bibles/niv-json.csv): CSV version of the "NIV Bible.json"
  - *Likely easier to just use the .json file*
- [Number of verses per chapter in Bible (KJV).xslsx](./Number of verses per chapter in Bible (KJV).xslsx): List of each book, it's chronological order, # of chapters, and then the # of verses per chapter.
  - *Note that this is the KJV. We probably want to use a different version.*
  - *The file includes some notes about manuscript differences. Make sure whatever we do we include details about that kind of thing!*
- [web_utf8_FINAL.xls](./Bibles/web_utf8_FINAL.xls): Basic excel file containing the WEB translation.
  - *Same format as the "kjv_apocrypha_utf8_FINAL.xls" file*
