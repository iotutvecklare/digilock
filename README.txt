# Säkerhetslås Projekt

Detta projekt implementerar ett säkerhetslås med en ESP32,
där användaren kan ange en kombination av knapptryckningar för att låsa upp ett servo (som simulerar ett lås).
Man kan också programmera en ny kombination.

## Komponenter

- ESP32
- 3 knappar för kombination
- 1 knapp för programmering
- 1 röd LED
- 1 grön LED
- 4 st 10k ohm resistorer för knappar
- 1 servo

## Kopplingsschema

Se den medföljande bilden för kopplingsschemat.

## Kod

Koden är skriven i MicroPython och finns i filen `lock_inlämning.py`.

## Funktioner

- **lock()**: Låser låset och tänder den röda LED:n.
- **unlock()**: Låser upp låset, tänder den gröna LED:n och återgår till låst läge efter 5 sekunder.
- **handle_button_press(button)**: Hanterar knapptryckningar och kontrollerar om kombinationen är korrekt.
- **check_combination()**: Kontrollerar om de senaste knapptryckningarna matchar den lagrade kombinationen.
- **save_combination_to_file()**: Sparar den aktuella kombinationen till en fil.
- **load_combination_from_file()**: Laddar kombinationen från en fil.
- **program_new_combination()**: Tillåter användaren att programmera en ny kombination.
- **setup()**: Initierar systemet genom att låsa låset och ladda kombinationen från fil.

## Instruktioner

1. **Anslut komponenterna enligt kopplingsschemat i bilden**.
2. **Ladda upp MicroPython-koden till ESP32**.
3. **Kör koden och kolla på seriella monitorn**.
4. **Tryck på knapparna** för att ange kombinationen   !!!!! (standardkombinationen är 1, 2, 3, 4). !!!!!
5. **Använd programmeringsknappen** för att ställa in en ny kombination och testa den nya kombinationen.

## Anmärkningar

Jag försökte köra detta projekt i Wowki, men jag fick det tyvärr inte att fungera.
Jag hoppas att detta duger ändå och att du kan se hur projektet är tänkt att fungera.
De vill också säga att det är faktiskt inte provat på riktigt men är snarlikt min teamate Aprils projekt.

Hannes Assarsson

