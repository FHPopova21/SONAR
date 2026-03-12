import { motion, AnimatePresence } from "motion/react";
import { LiquidCard } from "../components/ui/LiquidCard";
import { AudioVisualizer } from "../components/ui/AudioVisualizer";
import { Mic, Bell, Battery, Wifi, BellRing } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "../utils";

export function Dashboard() {
  const [isListening, setIsListening] = useState(false);
  const [statusText, setStatusText] = useState("Готовност за анализ");
  const [showToast, setShowToast] = useState(false);
  const [detectedSound, setDetectedSound] = useState<any>(null);

  // Излагаме функция към Eel, за да може Python да ни "бута" новини
  useEffect(() => {
    if (window.eel) {
      window.eel.expose(update_ui_result, "update_ui_result");
    }
  }, []);

  function update_ui_result(result: any) {
    const settings = JSON.parse(localStorage.getItem("sonar_settings") || '{"notifications":true}');

    if (result.status === "quiet") {
      setStatusText("Слушане на средата... ⏳");
      return;
    }

    const label = `Засечено: ${result.sound_type} (${result.confidence}%)`;
    setStatusText(result.status === "danger" ? `⚠️ ${label}` : label);
    setDetectedSound(result);

    // Показваме Toast ако са разрешени известията
    if (settings.notifications) {
      setShowToast(true);
      // Toast автоматично изчезва след 4.5 сек (преди следващия възможен анализ)
      setTimeout(() => setShowToast(false), 4500);
    }

    // След 5 секунди (колкото е cooldown на бекенда) връщаме статуса "Слушане"
    setTimeout(() => {
      setStatusText("Слушане на средата... ⏳");
    }, 5000);
  }

  const toggleListening = async () => {
    try {
      if (window.eel) {
        const nextState = !isListening;
        await window.eel.toggle_continuous_analysis(nextState)();
        setIsListening(nextState);

        if (nextState) {
          setStatusText("Слушане на средата... ⏳");
        } else {
          setStatusText("Анализът е спрян.");
        }
      }
    } catch (error) {
      console.error("Грешка при превключване на анализа:", error);
      setIsListening(false);
      setStatusText("Грешка при връзката");
    }
  };

  return (
    <div className="space-y-8 relative">
      {/* Main Status Card */}
      <LiquidCard className="flex flex-col items-center justify-center py-14 text-center">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: "spring", stiffness: 100 }}
          className="mb-8 flex items-center justify-center"
        >
          <AudioVisualizer isListening={isListening} />
        </motion.div>

        <h2 className="text-2xl font-bold text-slate-800 tracking-tight min-h-[3rem] flex items-center justify-center px-4">
          <AnimatePresence mode="wait">
            <motion.span
              key={statusText}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -5 }}
            >
              {statusText}
            </motion.span>
          </AnimatePresence>
        </h2>
        <p className="mt-2 max-w-[240px] text-sm font-medium text-slate-500 leading-relaxed">
          {isListening
            ? "Системата анализира звука в реално време."
            : "Натиснете бутона, за да стартирате постоянна защита."}
        </p>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={toggleListening}
          className={cn(
            "mt-8 rounded-2xl px-10 py-4 text-sm font-bold shadow-lg backdrop-blur-md transition-all",
            isListening
              ? "bg-red-500 text-white hover:bg-red-600 shadow-red-200"
              : "bg-emerald-500 text-white hover:bg-emerald-600 shadow-emerald-200"
          )}
        >
          {isListening ? "Спри анализа" : "Започни анализ"}
        </motion.button>
      </LiquidCard>

      {/* Toast Notification (Pop-up) */}
      <AnimatePresence>
        {showToast && detectedSound && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
            className="fixed bottom-24 left-6 right-6 z-50 pointer-events-none"
          >
            <div className="bg-white/90 backdrop-blur-xl border border-white/40 shadow-2xl rounded-3xl p-5 flex items-center gap-4 pointer-events-auto">
              <div className={cn(
                "h-12 w-12 rounded-2xl flex items-center justify-center shrink-0 shadow-sm",
                detectedSound.status === "danger" ? "bg-red-100 text-red-600" : "bg-blue-100 text-blue-600"
              )}>
                <BellRing size={24} />
              </div>
              <div>
                <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">
                  ЗАСЕЧЕН ЗВУК
                </div>
                <div className="font-bold text-slate-800 text-lg">
                  {detectedSound.sound_type}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Quick Status Row */}
      <div className="grid grid-cols-2 gap-4">
        <LiquidCard className="flex flex-col items-center p-5 text-center">
          <div className="mb-3 rounded-xl bg-green-100/50 p-2 text-green-600">
            <Battery size={22} />
          </div>
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Батерия</span>
          <span className="mt-1 text-xl font-black text-slate-800">84%</span>
        </LiquidCard>
        <LiquidCard className="flex flex-col items-center p-5 text-center">
          <div className="mb-3 rounded-xl bg-blue-100/50 p-2 text-blue-600">
            <Wifi size={22} />
          </div>
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Мрежа</span>
          <span className="mt-1 text-xl font-black text-slate-800">Стабилна</span>
        </LiquidCard>
      </div>

      {/* Recent Alerts Preview placeholder */}
      <div className="space-y-4">
        <div className="flex items-center justify-between px-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-[0.2em]">Последни събития</h3>
          <button className="text-[10px] font-bold text-blue-500 uppercase">Виж всички</button>
        </div>

        <div className="space-y-3">
          <LiquidCard className="flex items-center gap-5 p-5 transition-transform hover:scale-[1.01]">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 shadow-inner">
              <span className="text-2xl">🐕</span>
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-slate-800">Кучешки лай</h4>
              <p className="text-xs font-medium text-slate-400">Натиснете История за детайли</p>
            </div>
          </LiquidCard>
        </div>
      </div>
    </div>
  );
}
