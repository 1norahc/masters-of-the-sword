import { Badge } from "@/components/ui/badge"
import { Sword, Shield, Zap } from "lucide-react"
import type { GameStats } from "@/components/game-interface"

interface CharacterDisplayProps {
  stats: GameStats
}

export default function CharacterDisplay({ stats }: CharacterDisplayProps) {
  return (
    <div className="bg-slate-800 rounded-lg p-4 h-full flex flex-col md:flex-row items-center">
      <div className="relative mb-4 md:mb-0 md:mr-6">
        <div className="bg-slate-700 rounded-lg overflow-hidden w-40 h-40 flex items-center justify-center">
          <img src="/stoic-desert-guardian.png" alt="Character" className="w-full h-full object-cover" />
        </div>
        <Badge className="absolute -top-2 -right-2 bg-yellow-500">Poz. {stats.level}</Badge>
      </div>

      <div className="flex-1">
        <h2 className="text-xl font-bold mb-2">Wojownik</h2>
        <p className="text-gray-400 mb-4 text-sm">Odważny wojownik szukający chwały na arenie</p>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <Sword className="h-4 w-4 text-red-400" />
            <span className="text-gray-300">Siła</span>
            <span className="ml-auto font-bold">{stats.strength}</span>
          </div>

          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-blue-400" />
            <span className="text-gray-300">Obrona</span>
            <span className="ml-auto font-bold">{stats.defense}</span>
          </div>

          <div className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-yellow-400" />
            <span className="text-gray-300">Zręczność</span>
            <span className="ml-auto font-bold">{stats.agility}</span>
          </div>

          <div className="flex items-center gap-2">
            <div className="h-4 w-4 rounded-full bg-green-500"></div>
            <span className="text-gray-300">Wytrzymałość</span>
            <span className="ml-auto font-bold">{stats.stamina}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
