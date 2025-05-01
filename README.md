# WhereToGet

#Built with Python and Tkinter, packaged as a standalone Windows .exe using PyInstaller.

## 🛠 Build Instructions

You can rebuild the application yourself using PyInstaller.

### Step-by-step:

1. Install dependencies
   ```bash
   pip install pyinstaller tk

pyinstaller --noconfirm --onefile --windowed ^
    --add-data "Last Epoch uniques.txt;." ^
    --add-data "Last Epoch uniques (ru).txt;." ^
    unique_item_picker.py


A simple tool to help you find where to farm or obtain unique items in games like *Last Epoch*.  
Select an item and the app shows you how to get it — even multiple items at once!

## 🚀 Features
- Browse a list of unique items
- Click on any item to see detailed methods of obtaining
- Add multiple items to your selection
- Remove items by clicking anywhere on the card
- Search for items by name
- Switch between **English** and **Russian** interface
- Works offline (data is embedded into the app)
- Auto-saves selected items and language between sessions

## 📥 Downloads
- [v0.3](https://github.com/Kotington/WhereToGet/releases/tag/0.3) — Added Russian support, improved UI, fixed scrolling and multi-selection.

## Credits

This project uses data sourced from [lastepochtools.com](https://lastepochtools.com). A huge thank you to their team for gathering and providing this information.

## 🧑‍💻 Author
by Kotington  
Feel free to contribute!

---

# WhereToGet

Простой инструмент, который поможет найти способы получения уникальных предметов в играх, таких как *Last Epoch*.  
Выбери один или несколько предметов — и программа покажет, где их можно получить!

## 🚀 Возможности
- Список уникальных предметов
- Клик по карточке — показывает способы получения
- Выбор **нескольких предметов** одновременно
- Удаление предмета по клику на любую его часть
- Поиск по названию
- Переключение между **русским и английским языком**
- Работает без интернета (данные встроены в программу)
- Сохраняет выбранные предметы и язык между запусками

## 📥 Скачать
- [v0.3](https://github.com/Kotington/WhereToGet/releases/tag/0.3) — Добавлена поддержка русского языка, улучшен интерфейс, исправлен скроллинг и выбор нескольких предметов.

## 👨‍💻 Автор
Kotington  
Любые улучшения приветствуются!
