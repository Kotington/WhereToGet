# Changelog

## [v0.3] - 2025-04-07
### Added
- Full support for JSON item databases (`items_en.json`, `items_ru.json`)
- Language switching now reloads items correctly without data mismatches
- Improved hover detection on right panel cards (scrolling works anywhere: background, text, labels)
- Auto-save/load of selected items and current language
- Structured item grouping by `"type"` in JSON (e.g., Helmets, Weapons, Relics)

### Changed
- Rewrote resource path system to work properly with PyInstaller `.exe`
- Moved from raw TXT parsing to structured JSON format for easier updates
- Updated GUI card layout for better readability and interaction
- Optimized mousewheel scroll binding logic

### Fixed
- Scrolling didn't work when hovering over item name or obtained text in right panel
- Selected items list could show outdated names after language switch
- Items were not loading correctly in `.exe` due to wrong paths

### Known Issues
- Scrollbars may still behave slightly off during fast scrolling
- Language switch sometimes causes minor UI flicker before refresh

## [v0.2] - 2025-04-06
### Added
- Support for Russian language (switchable in UI)
- Improved custom scrollbar behavior
- Fixed scrolling issues on hover
- Better card click area (removal works on any part of the card)

### Changed
- Rewrote scroll binding system
- Improved layout spacing and responsiveness

### Known Issues
- Scrollbars may behave incorrectly during fast or sudden scrolling
- Selected items list might show outdated names after switching language due to different item databases

---

## [v0.1] - 2025-04-05
### Added
- Basic interface for selecting items
- Embedded item database (items from Last Epoch)
- Ability to search for items by name
- Windows .exe build included


# История изменений

## [v0.3] - 2025-04-07
### Добавлено
- Полная поддержка JSON баз данных (`items_en.json`, `items_ru.json`)
- При смене языка список предметов перезагружается корректно
- Прокрутка работает при наведении на **любые элементы карточки**: фон, текст, название, способ получения
- Автоматическое сохранение: язык и выбранные предметы сохраняются в `selected_items.json` и `settings.json`
- Предметы теперь сгруппированы по типу из JSON (например, "Шлем", "Реликвия")

### Изменено
- Переписана система `resource_path()` для лучшей совместимости с `.exe`
- Переход с `.txt` на `.json` — упрощает обновления и фильтрацию
- Обновление карточек в правом списке → более читабельный код

### Исправлено
- Прокрутка правого списка не работала при наведении на текст внутри карточки
- После смены языка отображались старые/неправильные данные
- Предметы не загружались в `.exe` из-за неверного пути к файлам

### Известные проблемы
- Скроллбары могут слегка дёргаться при быстрой прокрутке
- При смене языка возможен лёгкий мигающий эффект до обновления интерфейса

## [v0.2] - 2025-04-06
### Добавлено
- Поддержка русского языка (можно менять в интерфейсе)
- Улучшенное поведение кастомных скроллбаров
- Исправлены баги со скроллингом при наведении
- Теперь можно кликнуть в любое место карточки для удаления предмета

### Изменено
- Переписана система привязки скролла
- Улучшены отступы и отображение интерфейса

### Известные проблемы
- Скроллбары могут работать некорректно при резкой/быстрой прокрутке
- При смене языка список выбранных предметов может не совпадать с оригиналом (если перевод отличается)

---

## [v0.1] - 2025-04-05
### Добавлено
- Базовый интерфейс выбора предметов
- Встроенная база данных (уникальные предметы из Last Epoch)
- Возможность поиска по названию
- Сборка .exe для Windows