# Code Review - Geosoftware II     
# Checkliste  

**Quellen:**   

- https://nyu-cds.github.io/effective-code-reviews/03-checklist/
- https://www.liberty.edu/media/1414/%5B6401%5Dcode_review_checklist.pdf
- http://java.dzone.com/articles/java-code-review-checklist

**Struktur:**   
 
- Funktioniert der Code? (werden die Funktionen ausgeführt, ist die Logik korrekt?)
- Ist der Code leicht zu verstehen?
- Entspricht der Code den vereinbarten Codierungskonventionen? 
- Gibt es redundanten oder doppelten Code?
- Ist der Code so modular wie möglich?
- Ist der Code gut strukturiert, konsistent im Stil und konsistent formatiert?
- Gibt es nicht erreichbaren Code?
- Sind die Module übermäßig komplex und sollten neu strukturiert werden? 
- Ist der  Zugriff auf Pakete, Klassen, Schnittstellen, Methoden und Felder eingeschränkt?
- Beschränkung der Erweiterbarkeit von Klassen und Methoden und Feldern (final)?
- Ist der Code wartbar?
- Wird sichtbar, wer der jeweilige Autor (von Klassen oder Funktionen) ist?
- Werden Passwörter im Code gespeichert?

**Performance:**

- Kann Code durch Aufrufe von externen wiederverwendbaren Komponenten oder Bibliotheksfunktionen ersetzt werden?
- Gibt es offensichtliche Optimierungen, die die Leistung verbessern werden?
- Kann logging- oder debugging-Code entfernt werden?
- Werden unnötige Objekte erstellt?
- Werden alle verfügbaren Bibliotheken effektiv genutzt?

**Dokumentation:**

- Ist der Code einfach, klar und ausreichend kommentiert und dokumentiert?
- Stimmt der Inhalt der Kommentare mit dem Code überein?

**Variablen:**

- Sind alle Variablen mit aussagekräftigen, konsistenten und klaren Namen richtig definiert?
- Gibt es redundante oder nicht verwendete Variablen?

**Arithmetische Operationen:**

- Verhindert der Code den Vergleich von Gleitkommazahlen auf Gleichheit?
- Verhindert der Code systematisch Rundungsfehler?
- Werden Divisionen auf Null geprüft?
- Werden Objekte gecastet und wenn ja, werden sie richtig gecastet?

**Schleifen und Zweige (Branches):**

- Sind alle Schleifen, Verzweigungen und Logikkonstrukte vollständig, korrekt und richtig verschachtelt?
- Werden die häufigsten Fälle zuerst in IF-ELSEIF-Ketten getestet?
- Sind Bedingungen für die Beendigung der Schleife naheliegend und immer erreichbar?
- Werden Indizes direkt vor der Schleife ordnungsgemäß initialisiert?
- Können Aussagen innerhalb von Schleifen außerhalb der Schleifen platziert werden?
- Gibt es Endlosschleifen?

**Testen:**

- Sind valide und ausreichende Tests vorhanden (ggfs. Pytest für Python)?
