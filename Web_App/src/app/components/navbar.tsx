import { motion } from "motion/react";
import { Volume2 } from "lucide-react";

export function Navbar() {

  return (
    <motion.nav 
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 z-50 px-6 py-4 lg:px-12 backdrop-blur-xl bg-[#0f0620]/60 border-b border-white/[0.05]"
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <a href="#" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#ff6b35] to-[#ec4899] flex items-center justify-center shadow-[0_0_15px_rgba(255,107,53,0.4)]">
            <Volume2 className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold tracking-widest text-lg text-white">SONAR</span>
        </a>
        
        <div className="hidden md:flex gap-8 text-sm font-medium text-white/60">
          <a href="#problem" className="hover:text-white transition-colors">Проблемът</a>
          <a href="#how-it-works" className="hover:text-white transition-colors">Как работи</a>
          <a href="#demo" className="hover:text-white transition-colors">Демонстрация</a>
          <a href="#tech" className="hover:text-white transition-colors">Технологии</a>
        </div>
        
        <button className="relative group px-6 py-2 bg-white/[0.05] hover:bg-white/[0.1] border border-white/10 backdrop-blur-xl rounded-[1.5rem] transition-all duration-300 shadow-[inset_0_0_15px_rgba(255,255,255,0.02)]">
          <div className="absolute inset-0 bg-gradient-to-r from-[#ff6b35]/20 to-[#ec4899]/20 rounded-[1.5rem] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          <span className="relative text-white font-medium text-sm">
            Изтегли
          </span>
        </button>
      </div>
    </motion.nav>
  );
}
