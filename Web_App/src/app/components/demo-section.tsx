import { motion } from "motion/react";
import { Play, Volume2, AlertTriangle } from "lucide-react";
import { useState } from "react";

export function DemoSection() {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <section className="relative py-24 px-6 md:px-12 lg:px-24 overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[600px] bg-gradient-to-r from-[#a855f7] via-[#ec4899] to-[#ff6b35] opacity-10 blur-[200px]" />

      <div className="relative z-10 max-w-6xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 space-y-4"
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl tracking-tight" style={{ fontWeight: 800 }}>
            Виж го в действие
          </h2>
          <p className="text-lg md:text-xl opacity-70 max-w-2xl mx-auto">
            Демонстрация на разпознаването на сирени в реално време
          </p>
        </motion.div>

        {/* Video Player Container */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="relative group"
        >
          {/* Outer Glow */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#ff6b35] via-[#ec4899] to-[#a855f7] opacity-0 group-hover:opacity-30 transition-opacity duration-500 rounded-[2rem] blur-3xl" />

          {/* Glass Frame */}
          <div className="relative backdrop-blur-xl bg-white/[0.05] border-2 border-white/10 rounded-[2rem] p-4 shadow-2xl">
            {/* Video Display Area */}
            <div className="relative aspect-video bg-gradient-to-br from-purple-950/50 to-black rounded-2xl overflow-hidden">
              {/* Placeholder Video Content */}
              <div className="absolute inset-0 flex items-center justify-center">
                {!isPlaying ? (
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setIsPlaying(true)}
                    className="w-24 h-24 rounded-full bg-gradient-to-br from-[#ff6b35] to-[#ec4899] flex items-center justify-center shadow-[0_0_60px_rgba(255,107,53,0.6)] hover:shadow-[0_0_80px_rgba(255,107,53,0.8)] transition-all duration-300"
                  >
                    <Play className="w-10 h-10 text-white fill-white ml-1" />
                  </motion.button>
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center gap-8 p-12">
                    {/* Alert Indicator */}
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="backdrop-blur-xl bg-red-500/20 border-2 border-red-500 rounded-3xl px-8 py-6 flex items-center gap-4"
                    >
                      <motion.div
                        animate={{
                          rotate: [0, 10, -10, 0],
                        }}
                        transition={{
                          duration: 0.5,
                          repeat: Infinity,
                        }}
                      >
                        <AlertTriangle className="w-12 h-12 text-red-500" />
                      </motion.div>
                      <div>
                        <div className="text-3xl mb-1" style={{ fontWeight: 700 }}>
                          Сирена: 95%
                        </div>
                        <div className="text-sm opacity-70">Разпозната заплаха</div>
                      </div>
                    </motion.div>

                    {/* Audio Visualization */}
                    <div className="flex items-center gap-6">
                      <Volume2 className="w-8 h-8 text-[#ff6b35]" />
                      <div className="flex items-end gap-1 h-24">
                        {Array.from({ length: 50 }).map((_, i) => (
                          <motion.div
                            key={i}
                            className="w-2 bg-gradient-to-t from-[#ff6b35] to-[#ec4899] rounded-full"
                            animate={{
                              height: [
                                `${30 + Math.random() * 50}%`,
                                `${40 + Math.random() * 60}%`,
                                `${30 + Math.random() * 50}%`,
                              ],
                            }}
                            transition={{
                              duration: 0.3 + Math.random() * 0.4,
                              repeat: Infinity,
                              ease: "easeInOut",
                            }}
                          />
                        ))}
                      </div>
                    </div>

                    {/* Status Info */}
                    <div className="grid grid-cols-3 gap-6 w-full max-w-2xl">
                      {[
                        { label: "Латентност", value: "12ms" },
                        { label: "Точност", value: "95.2%" },
                        { label: "Модел", value: "MobileNetV2" },
                      ].map((stat, i) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.3 + i * 0.1 }}
                          className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-4 text-center"
                        >
                          <div className="text-2xl mb-1" style={{ fontWeight: 700, color: "#ff6b35" }}>
                            {stat.value}
                          </div>
                          <div className="text-sm opacity-60">{stat.label}</div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Decorative Grid Overlay */}
              <div className="absolute inset-0 opacity-5 pointer-events-none">
                <div className="w-full h-full" style={{
                  backgroundImage: "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
                  backgroundSize: "50px 50px"
                }} />
              </div>
            </div>

            {/* Control Bar */}
            <div className="mt-4 flex items-center justify-between px-4">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.8)] animate-pulse" />
                <span className="text-sm opacity-60">Live Demo</span>
              </div>
              {isPlaying && (
                <motion.button
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setIsPlaying(false)}
                  className="px-4 py-2 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 text-sm hover:bg-white/20 transition-all"
                  style={{ fontWeight: 600 }}
                >
                  Рестарт
                </motion.button>
              )}
            </div>
          </div>
        </motion.div>

        {/* Feature Highlights */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-12 grid md:grid-cols-2 gap-6"
        >
          {[
            {
              title: "Реално време",
              description: "Анализ и известяване под 20 милисекунди",
              icon: "⚡",
            },
            {
              title: "Висока точност",
              description: "95%+ успеваемост при класифициране на звуци",
              icon: "🎯",
            },
          ].map((feature, i) => (
            <div
              key={i}
              className="backdrop-blur-xl bg-white/[0.05] border border-white/10 rounded-2xl p-6 flex items-center gap-4"
            >
              <div className="text-4xl">{feature.icon}</div>
              <div>
                <h4 className="mb-1" style={{ fontWeight: 700 }}>
                  {feature.title}
                </h4>
                <p className="text-sm opacity-70">{feature.description}</p>
              </div>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
