import { Flame, Heart, Trophy, Zap } from "lucide-react";
import { motion } from "motion/react";

const MAX_LIVES = 5;

export default function GameHud({ level, xp, streak, lives }) {
  return (
    <motion.header
      className="game-hud"
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
    >
      <div className="hud-brand">
        <div className="game-logo-wrap">
          <h1 className="game-logo">
            SQL <span>Quest</span>
          </h1>
        </div>
      </div>

      <div className="hud-stats" aria-label="Status do jogador">
        <div className="hud-stat level-stat">
          <Trophy size={17} />
          <span>Nível {level}</span>
        </div>
        <div className="hud-stat xp-stat">
          <Zap size={17} />
          <span>{xp}/100 XP</span>
        </div>
        <div className="hud-stat streak-stat">
          <Flame size={17} />
          <span>Sequência {streak}</span>
        </div>
        <div className="hud-lives" aria-label={`${lives} de ${MAX_LIVES} vidas`}>
          {Array.from({ length: MAX_LIVES }, (_, index) => (
            <Heart
              key={index}
              className={index < lives ? "heart active" : "heart lost"}
              size={22}
              fill="currentColor"
              aria-hidden="true"
            />
          ))}
        </div>
      </div>
    </motion.header>
  );
}
