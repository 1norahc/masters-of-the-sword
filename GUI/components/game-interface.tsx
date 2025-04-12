"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sword, Shield, Users, Scroll, Heart, Zap, Coins, LogOut, Store } from "lucide-react"
import CharacterDisplay from "@/components/character-display"
import EquipmentPanel from "@/components/equipment-panel"
import CombatPanel from "@/components/combat-panel"
import QuestPanel from "@/components/quest-panel"
import ShopPanel from "@/components/shop-panel"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import LevelUpModal from "@/components/level-up-modal"

// Eksportujemy typ dla kontekstu gry
export type GameStats = {
  gold: number
  level: number
  experience: number
  maxExperience: number
  health: number
  maxHealth: number
  energy: number
  maxEnergy: number
  strength: number
  defense: number
  agility: number
  stamina: number
}

export default function GameInterface() {
  const [stats, setStats] = useState<GameStats>({
    gold: 250,
    level: 1,
    experience: 35,
    maxExperience: 100,
    health: 85,
    maxHealth: 100,
    energy: 75,
    maxEnergy: 100,
    strength: 24,
    defense: 18,
    agility: 15,
    stamina: 22,
  })

  const [showLevelUp, setShowLevelUp] = useState(false)
  const [availablePoints, setAvailablePoints] = useState(0)
  const router = useRouter()
  const { toast } = useToast()

  // Funkcja do dodawania doświadczenia
  const addExperience = (amount: number) => {
    setStats((prev) => {
      const newExperience = prev.experience + amount

      // Sprawdzamy czy nastąpił awans na wyższy poziom
      if (newExperience >= prev.maxExperience) {
        // Obliczamy nadmiarowe doświadczenie
        const overflow = newExperience - prev.maxExperience

        // Zwiększamy poziom i resetujemy doświadczenie
        const newLevel = prev.level + 1

        // Zwiększamy maksymalne doświadczenie dla nowego poziomu
        const newMaxExperience = Math.floor(prev.maxExperience * 1.5)

        // Zwiększamy statystyki za awans
        const newMaxHealth = prev.maxHealth + 10
        const newMaxEnergy = prev.maxEnergy + 5

        // Dodajemy punkty umiejętności
        setAvailablePoints((prev) => prev + 5)

        // Pokazujemy modal awansu
        setShowLevelUp(true)

        // Wyświetlamy toast z informacją o awansie
        toast({
          title: "Awans na wyższy poziom!",
          description: `Osiągnąłeś poziom ${newLevel}! Otrzymujesz 5 punktów umiejętności.`,
          variant: "default",
        })

        return {
          ...prev,
          level: newLevel,
          experience: overflow,
          maxExperience: newMaxExperience,
          health: newMaxHealth, // Pełne zdrowie po awansie
          maxHealth: newMaxHealth,
          energy: newMaxEnergy, // Pełna energia po awansie
          maxEnergy: newMaxEnergy,
        }
      }

      return {
        ...prev,
        experience: newExperience,
      }
    })
  }

  // Funkcja do dodawania złota
  const addGold = (amount: number) => {
    setStats((prev) => ({
      ...prev,
      gold: prev.gold + amount,
    }))

    toast({
      title: "Otrzymano złoto",
      description: `Otrzymano ${amount} sztuk złota.`,
      variant: "default",
    })
  }

  // Funkcja do wydawania złota
  const spendGold = (amount: number): boolean => {
    if (stats.gold >= amount) {
      setStats((prev) => ({
        ...prev,
        gold: prev.gold - amount,
      }))
      return true
    }

    toast({
      title: "Niewystarczająca ilość złota",
      description: "Nie masz wystarczającej ilości złota, aby dokonać zakupu.",
      variant: "destructive",
    })
    return false
  }

  // Funkcja do zwiększania statystyk
  const increaseStats = (stat: keyof GameStats, amount = 1) => {
    if (availablePoints > 0) {
      setStats((prev) => ({
        ...prev,
        [stat]: prev[stat] + amount,
      }))

      setAvailablePoints((prev) => prev - 1)
    }
  }

  const handleLogout = () => {
    router.push("/")
  }

  return (
    <div className="container mx-auto p-4 max-w-6xl">
      {/* Game Header */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-2">
          <img src="/stylized-sword-emblem.png" alt="Master of the Sword" className="h-16 w-16" />
          <h1 className="text-3xl font-bold text-yellow-400">Władca Miecza</h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Coins className="h-5 w-5 text-yellow-400" />
            <span className="font-bold">{stats.gold}</span>
          </div>
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" className="border-yellow-500 text-yellow-400 hover:bg-yellow-500/20">
                <Store className="h-5 w-5 mr-2" />
                Sklep
              </Button>
            </SheetTrigger>
            <SheetContent className="bg-slate-800 border-slate-700 text-white overflow-y-auto" side="right">
              <ShopPanel gold={stats.gold} spendGold={spendGold} level={stats.level} />
            </SheetContent>
          </Sheet>
          <Button variant="ghost" size="icon" onClick={handleLogout}>
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Character Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-slate-800 rounded-lg p-4 col-span-1">
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Poziom {stats.level}</span>
              <span className="text-xs text-gray-400">
                {stats.experience}/{stats.maxExperience} PD
              </span>
            </div>
            <Progress
              value={(stats.experience / stats.maxExperience) * 100}
              className="h-2 bg-gray-700"
              indicatorClassName="bg-purple-500"
            />

            <div className="flex justify-between items-center">
              <div className="flex items-center gap-1">
                <Heart className="h-4 w-4 text-red-500" />
                <span className="text-gray-300">Zdrowie</span>
              </div>
              <span className="text-xs text-gray-400">
                {stats.health}/{stats.maxHealth}
              </span>
            </div>
            <Progress
              value={(stats.health / stats.maxHealth) * 100}
              className="h-2 bg-gray-700"
              indicatorClassName="bg-red-500"
            />

            <div className="flex justify-between items-center">
              <div className="flex items-center gap-1">
                <Zap className="h-4 w-4 text-blue-400" />
                <span className="text-gray-300">Energia</span>
              </div>
              <span className="text-xs text-gray-400">
                {stats.energy}/{stats.maxEnergy}
              </span>
            </div>
            <Progress
              value={(stats.energy / stats.maxEnergy) * 100}
              className="h-2 bg-gray-700"
              indicatorClassName="bg-blue-400"
            />

            {availablePoints > 0 && (
              <Button
                variant="outline"
                size="sm"
                className="mt-2 border-yellow-500 text-yellow-400 hover:bg-yellow-500/20"
                onClick={() => setShowLevelUp(true)}
              >
                Dostępne punkty: {availablePoints}
              </Button>
            )}
          </div>
        </div>

        <div className="col-span-2">
          <CharacterDisplay stats={stats} />
        </div>
      </div>

      {/* Game Navigation */}
      <Tabs defaultValue="combat" className="w-full">
        <TabsList className="grid grid-cols-4 h-auto bg-slate-800 p-1">
          <TabsTrigger value="combat" className="py-3 data-[state=active]:bg-slate-700">
            <Sword className="h-5 w-5 mr-2" />
            Walka
          </TabsTrigger>
          <TabsTrigger value="equipment" className="py-3 data-[state=active]:bg-slate-700">
            <Shield className="h-5 w-5 mr-2" />
            Ekwipunek
          </TabsTrigger>
          <TabsTrigger value="quests" className="py-3 data-[state=active]:bg-slate-700">
            <Scroll className="h-5 w-5 mr-2" />
            Zadania
          </TabsTrigger>
          <TabsTrigger value="tavern" className="py-3 data-[state=active]:bg-slate-700">
            <Users className="h-5 w-5 mr-2" />
            Karczma
          </TabsTrigger>
        </TabsList>

        <TabsContent value="combat" className="mt-4">
          <CombatPanel
            playerStats={stats}
            addExperience={addExperience}
            addGold={addGold}
            setPlayerHealth={(health: number) => setStats((prev) => ({ ...prev, health }))}
          />
        </TabsContent>

        <TabsContent value="equipment" className="mt-4">
          <EquipmentPanel />
        </TabsContent>

        <TabsContent value="quests" className="mt-4">
          <QuestPanel addExperience={addExperience} addGold={addGold} />
        </TabsContent>

        <TabsContent value="tavern" className="mt-4">
          <div className="bg-slate-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Karczma</h2>
            <p className="text-gray-300 mb-4">
              Spotykaj innych graczy, dołączaj do gildii i znajdź towarzyszy do swoich przygód!
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-700 p-4 rounded-lg">
                <h3 className="font-bold text-yellow-400 mb-2">Najlepsi Gracze</h3>
                <ul className="space-y-2">
                  {["ZabójcaSmoków", "MistrzMiecza", "KrólRycerzy", "TancerzOstrzy", "NosicielTarczy"].map(
                    (name, index) => (
                      <li key={index} className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <span className="text-gray-400">{index + 1}.</span>
                          <span>{name}</span>
                        </div>
                        <span className="text-gray-400">Poz. {Math.floor(Math.random() * 50) + 20}</span>
                      </li>
                    ),
                  )}
                </ul>
              </div>

              <div className="bg-slate-700 p-4 rounded-lg">
                <h3 className="font-bold text-yellow-400 mb-2">Aktywne Gildie</h3>
                <ul className="space-y-2">
                  {["Żelazne Ostrza", "Złoci Rycerze", "Cieniste Zabójcy", "Królewska Gwardia", "Łowcy Smoków"].map(
                    (name, index) => (
                      <li key={index} className="flex justify-between items-center">
                        <span>{name}</span>
                        <Button variant="outline" size="sm" className="h-7 text-xs">
                          Dołącz
                        </Button>
                      </li>
                    ),
                  )}
                </ul>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Modal awansu na wyższy poziom */}
      {showLevelUp && (
        <LevelUpModal
          isOpen={showLevelUp}
          onClose={() => setShowLevelUp(false)}
          stats={stats}
          availablePoints={availablePoints}
          increaseStats={increaseStats}
        />
      )}
    </div>
  )
}
