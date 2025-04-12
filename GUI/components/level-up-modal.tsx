"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Sword, Shield, Zap, Heart } from "lucide-react"
import type { GameStats } from "@/components/game-interface"

interface LevelUpModalProps {
  isOpen: boolean
  onClose: () => void
  stats: GameStats
  availablePoints: number
  increaseStats: (stat: keyof GameStats, amount?: number) => void
}

export default function LevelUpModal({ isOpen, onClose, stats, availablePoints, increaseStats }: LevelUpModalProps) {
  const [localStats, setLocalStats] = useState({
    strength: 0,
    defense: 0,
    agility: 0,
    stamina: 0,
  })
  const [remainingPoints, setRemainingPoints] = useState(availablePoints)

  const handleIncrease = (stat: "strength" | "defense" | "agility" | "stamina") => {
    if (remainingPoints > 0) {
      setLocalStats((prev) => ({
        ...prev,
        [stat]: prev[stat] + 1,
      }))
      setRemainingPoints((prev) => prev - 1)
    }
  }

  const handleDecrease = (stat: "strength" | "defense" | "agility" | "stamina") => {
    if (localStats[stat] > 0) {
      setLocalStats((prev) => ({
        ...prev,
        [stat]: prev[stat] - 1,
      }))
      setRemainingPoints((prev) => prev + 1)
    }
  }

  const handleConfirm = () => {
    // Zwiększamy statystyki
    if (localStats.strength > 0) increaseStats("strength", localStats.strength)
    if (localStats.defense > 0) increaseStats("defense", localStats.defense)
    if (localStats.agility > 0) increaseStats("agility", localStats.agility)
    if (localStats.stamina > 0) increaseStats("stamina", localStats.stamina)

    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="bg-slate-800 border-slate-700 text-white">
        <DialogHeader>
          <DialogTitle className="text-2xl text-yellow-400">Awans na poziom {stats.level}!</DialogTitle>
          <DialogDescription className="text-gray-300">
            Gratulacje! Awansowałeś na wyższy poziom. Rozdziel punkty umiejętności, aby zwiększyć swoje statystyki.
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <div className="text-center mb-4">
            <span className="text-lg font-bold text-yellow-400">Dostępne punkty: {remainingPoints}</span>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between bg-slate-700 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <Sword className="h-5 w-5 text-red-400" />
                <span>Siła</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-300">{stats.strength}</span>
                <span className="text-green-400">+{localStats.strength}</span>
                <div className="flex gap-1">
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleDecrease("strength")}
                    disabled={localStats.strength <= 0}
                  >
                    -
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleIncrease("strength")}
                    disabled={remainingPoints <= 0}
                  >
                    +
                  </Button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between bg-slate-700 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-blue-400" />
                <span>Obrona</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-300">{stats.defense}</span>
                <span className="text-green-400">+{localStats.defense}</span>
                <div className="flex gap-1">
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleDecrease("defense")}
                    disabled={localStats.defense <= 0}
                  >
                    -
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleIncrease("defense")}
                    disabled={remainingPoints <= 0}
                  >
                    +
                  </Button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between bg-slate-700 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-yellow-400" />
                <span>Zręczność</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-300">{stats.agility}</span>
                <span className="text-green-400">+{localStats.agility}</span>
                <div className="flex gap-1">
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleDecrease("agility")}
                    disabled={localStats.agility <= 0}
                  >
                    -
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleIncrease("agility")}
                    disabled={remainingPoints <= 0}
                  >
                    +
                  </Button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between bg-slate-700 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <Heart className="h-5 w-5 text-green-400" />
                <span>Wytrzymałość</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-300">{stats.stamina}</span>
                <span className="text-green-400">+{localStats.stamina}</span>
                <div className="flex gap-1">
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleDecrease("stamina")}
                    disabled={localStats.stamina <= 0}
                  >
                    -
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => handleIncrease("stamina")}
                    disabled={remainingPoints <= 0}
                  >
                    +
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Anuluj
          </Button>
          <Button onClick={handleConfirm}>Potwierdź</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
