-- Languages.lua  -  text for the Language setting of Adaptive Clock   (save this file as UTF-8)
-- Author: Amika Alankara  (MIT License)
--
-- English is built into AdaptiveClock.lua. Add a language by copying a block below, translating it, and adding its
-- name to the language list in AdaptiveClock.lua (CycleLanguage) and Settings.ini. Missing keys fall back to English.
--   dow / dowS / dowH   weekday: full / short / calendar header (Sunday first)
--   mon / monS          month: full / short
--   greet               night, morning, afternoon, evening
--   t                   labels ({n} = number, {year} = year)

return {

Spanish = {
  dow  = { 'domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado' },
  dowS = { 'Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb' },
  dowH = { 'Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá' },
  mon  = { 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre' },
  monS = { 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic' },
  greet = { night = 'Buenas noches', morning = 'Buenos días', afternoon = 'Buenas tardes', evening = 'Buenas noches' },
  t = { hour = 'HORA', minute = 'MINUTO', second = 'SEGUNDO', hours = 'HORAS', minutes = 'MINUTOS', seconds = 'SEGUNDOS',
        world = 'Hora mundial', daysLeft = '{n} días restantes', daysLeftYear = 'Quedan {n} días en {year}',
        yearDone = 'de {year} completado', ofYear = 'de {year}', secondsLow = 'segundos', focus = 'ENFOQUE', rest = 'DESCANSO',
        alarm = 'Alarma', ringing = '¡ALARMA!', sunrise = 'Amanecer', sunset = 'Atardecer',
        nothing = 'Nada en reproducción', battery = 'Batería', charging = 'Cargando' },
},

French = {
  dow  = { 'dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi' },
  dowS = { 'dim', 'lun', 'mar', 'mer', 'jeu', 'ven', 'sam' },
  dowH = { 'Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa' },
  mon  = { 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre' },
  monS = { 'janv', 'févr', 'mars', 'avr', 'mai', 'juin', 'juil', 'août', 'sept', 'oct', 'nov', 'déc' },
  greet = { night = 'Bonne nuit', morning = 'Bonjour', afternoon = 'Bon après-midi', evening = 'Bonsoir' },
  t = { hour = 'HEURE', minute = 'MINUTE', second = 'SECONDE', hours = 'HEURES', minutes = 'MINUTES', seconds = 'SECONDES',
        world = 'Heure mondiale', daysLeft = '{n} jours restants', daysLeftYear = 'Encore {n} jours en {year}',
        yearDone = 'de {year} écoulé', ofYear = 'de {year}', secondsLow = 'secondes', focus = 'CONCENTRATION', rest = 'PAUSE',
        alarm = 'Alarme', ringing = 'ALARME !', sunrise = 'Lever du soleil', sunset = 'Coucher du soleil',
        nothing = 'Aucune lecture', battery = 'Batterie', charging = 'En charge' },
},

German = {
  dow  = { 'Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag' },
  dowS = { 'So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa' },
  dowH = { 'So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa' },
  mon  = { 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember' },
  monS = { 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez' },
  greet = { night = 'Gute Nacht', morning = 'Guten Morgen', afternoon = 'Guten Tag', evening = 'Guten Abend' },
  t = { hour = 'STUNDE', minute = 'MINUTE', second = 'SEKUNDE', hours = 'STUNDEN', minutes = 'MINUTEN', seconds = 'SEKUNDEN',
        world = 'Weltzeit', daysLeft = 'noch {n} Tage', daysLeftYear = 'noch {n} Tage in {year}',
        yearDone = 'von {year} geschafft', ofYear = 'von {year}', secondsLow = 'Sekunden', focus = 'FOKUS', rest = 'PAUSE',
        alarm = 'Wecker', ringing = 'WECKER!', sunrise = 'Sonnenaufgang', sunset = 'Sonnenuntergang',
        nothing = 'Nichts spielt', battery = 'Akku', charging = 'Lädt' },
},

Portuguese = {
  dow  = { 'domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado' },
  dowS = { 'Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb' },
  dowH = { 'Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb' },
  mon  = { 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro' },
  monS = { 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez' },
  greet = { night = 'Boa noite', morning = 'Bom dia', afternoon = 'Boa tarde', evening = 'Boa noite' },
  t = { hour = 'HORA', minute = 'MINUTO', second = 'SEGUNDO', hours = 'HORAS', minutes = 'MINUTOS', seconds = 'SEGUNDOS',
        world = 'Hora mundial', daysLeft = '{n} dias restantes', daysLeftYear = 'Faltam {n} dias em {year}',
        yearDone = 'de {year} concluído', ofYear = 'de {year}', secondsLow = 'segundos', focus = 'FOCO', rest = 'PAUSA',
        alarm = 'Alarme', ringing = 'ALARME!', sunrise = 'Nascer do sol', sunset = 'Pôr do sol',
        nothing = 'Nada a tocar', battery = 'Bateria', charging = 'A carregar' },
},

Italian = {
  dow  = { 'domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato' },
  dowS = { 'Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab' },
  dowH = { 'Do', 'Lu', 'Ma', 'Me', 'Gi', 'Ve', 'Sa' },
  mon  = { 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre' },
  monS = { 'gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic' },
  greet = { night = 'Buonanotte', morning = 'Buongiorno', afternoon = 'Buon pomeriggio', evening = 'Buonasera' },
  t = { hour = 'ORA', minute = 'MINUTO', second = 'SECONDO', hours = 'ORE', minutes = 'MINUTI', seconds = 'SECONDI',
        world = 'Ora mondiale', daysLeft = '{n} giorni rimanenti', daysLeftYear = 'Restano {n} giorni nel {year}',
        yearDone = 'del {year} completato', ofYear = 'del {year}', secondsLow = 'secondi', focus = 'FOCUS', rest = 'PAUSA',
        alarm = 'Sveglia', ringing = 'SVEGLIA!', sunrise = 'Alba', sunset = 'Tramonto',
        nothing = 'Nessuna riproduzione', battery = 'Batteria', charging = 'In carica' },
},

Sinhala = {
  dow  = { 'ඉරිදා', 'සඳුදා', 'අඟහරුවාදා', 'බදාදා', 'බ්‍රහස්පතින්දා', 'සිකුරාදා', 'සෙනසුරාදා' },
  dowS = { 'ඉරි', 'සඳු', 'අඟ', 'බදා', 'බ්‍රහ', 'සිකු', 'සෙන' },
  dowH = { 'ඉරි', 'සඳු', 'අඟ', 'බදා', 'බ්‍රහ', 'සිකු', 'සෙන' },
  mon  = { 'ජනවාරි', 'පෙබරවාරි', 'මාර්තු', 'අප්‍රේල්', 'මැයි', 'ජූනි', 'ජූලි', 'අගෝස්තු', 'සැප්තැම්බර්', 'ඔක්තෝබර්', 'නොවැම්බර්', 'දෙසැම්බර්' },
  monS = { 'ජන', 'පෙබ', 'මාර්', 'අප්‍රේ', 'මැයි', 'ජූනි', 'ජූලි', 'අගෝ', 'සැප්', 'ඔක්', 'නොවැ', 'දෙසැ' },
  greet = { night = 'සුභ රාත්‍රියක්', morning = 'සුභ උදෑසනක්', afternoon = 'සුභ දහවලක්', evening = 'සුභ සන්ධ්‍යාවක්' },
  t = { hour = 'පැය', minute = 'මිනිත්තුව', second = 'තත්පරය', hours = 'පැය', minutes = 'මිනිත්තු', seconds = 'තත්පර',
        world = 'ලෝක වේලාව', daysLeft = 'දින {n}ක් ඉතිරියි', daysLeftYear = '{year} වසරේ දින {n}ක් ඉතිරියි',
        yearDone = '{year} වසරෙන් ගතවූයේ', ofYear = '{year} වසරෙන්', secondsLow = 'තත්පර', focus = 'අවධානය', rest = 'විවේකය',
        alarm = 'ඇලාරම', ringing = 'ඇලාරම!', sunrise = 'හිරු උදාව', sunset = 'හිරු බැසීම',
        nothing = 'කිසිවක් වාදනය නොවේ', battery = 'බැටරිය', charging = 'ආරෝපණය වෙමින්' },
},

Tamil = {
  dow  = { 'ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி' },
  dowS = { 'ஞாயி', 'திங்', 'செவ்', 'புத', 'வியா', 'வெள்', 'சனி' },
  dowH = { 'ஞா', 'தி', 'செ', 'பு', 'வி', 'வெ', 'ச' },
  mon  = { 'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்', 'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்' },
  monS = { 'ஜன', 'பிப்', 'மார்', 'ஏப்', 'மே', 'ஜூன்', 'ஜூலை', 'ஆக', 'செப்', 'அக்', 'நவ', 'டிச' },
  greet = { night = 'இனிய இரவு', morning = 'காலை வணக்கம்', afternoon = 'மதிய வணக்கம்', evening = 'மாலை வணக்கம்' },
  t = { hour = 'மணி', minute = 'நிமிடம்', second = 'விநாடி', hours = 'மணி', minutes = 'நிமிடங்கள்', seconds = 'விநாடிகள்',
        world = 'உலக நேரம்', daysLeft = '{n} நாட்கள் மீதம்', daysLeftYear = '{year} ஆண்டில் {n} நாட்கள் மீதம்',
        yearDone = '{year} இல் கடந்தது', ofYear = '{year} இல்', secondsLow = 'விநாடிகள்', focus = 'கவனம்', rest = 'ஓய்வு',
        alarm = 'அலாரம்', ringing = 'அலாரம்!', sunrise = 'சூரிய உதயம்', sunset = 'சூரிய அஸ்தமனம்',
        nothing = 'எதுவும் இயங்கவில்லை', battery = 'மின்கலம்', charging = 'சார்ஜ் ஆகிறது' },
},

Hindi = {
  dow  = { 'रविवार', 'सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार' },
  dowS = { 'रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि' },
  dowH = { 'रवि', 'सोम', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि' },
  mon  = { 'जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर' },
  monS = { 'जन', 'फ़र', 'मार्च', 'अप्रै', 'मई', 'जून', 'जुला', 'अग', 'सित', 'अक्टू', 'नव', 'दिस' },
  greet = { night = 'शुभ रात्रि', morning = 'सुप्रभात', afternoon = 'शुभ दोपहर', evening = 'शुभ संध्या' },
  t = { hour = 'घंटा', minute = 'मिनट', second = 'सेकंड', hours = 'घंटे', minutes = 'मिनट', seconds = 'सेकंड',
        world = 'विश्व समय', daysLeft = '{n} दिन बाकी', daysLeftYear = '{year} में {n} दिन बाकी',
        yearDone = '{year} का बीता हिस्सा', ofYear = '{year} में से', secondsLow = 'सेकंड', focus = 'फोकस', rest = 'विश्राम',
        alarm = 'अलार्म', ringing = 'अलार्म!', sunrise = 'सूर्योदय', sunset = 'सूर्यास्त',
        nothing = 'कुछ नहीं बज रहा', battery = 'बैटरी', charging = 'चार्ज हो रही है' },
},

Japanese = {
  dow  = { '日曜日', '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日' },
  dowS = { '日', '月', '火', '水', '木', '金', '土' },
  dowH = { '日', '月', '火', '水', '木', '金', '土' },
  mon  = { '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月' },
  monS = { '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月' },
  greet = { night = 'おやすみなさい', morning = 'おはようございます', afternoon = 'こんにちは', evening = 'こんばんは' },
  t = { hour = '時', minute = '分', second = '秒', hours = '時', minutes = '分', seconds = '秒',
        world = '世界時計', daysLeft = '残り{n}日', daysLeftYear = '{year}年の残り{n}日',
        yearDone = '{year}年の経過', ofYear = '{year}年', secondsLow = '秒', focus = '集中', rest = '休憩',
        alarm = 'アラーム', ringing = 'アラーム!', sunrise = '日の出', sunset = '日の入り',
        nothing = '再生なし', battery = 'バッテリー', charging = '充電中' },
},

}
