"use client"

import type { GameStats } from "@/components/game-interface"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Sword, Shield, Zap, Bot, User } from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useToast } from "@/hooks/use-toast"

// Typy przeciwników
const enemies = [
  {
    id: "gladiator",
    name: "Gladiator",
    health: 100,
    damage: [3, 10],
    image: "/arena-foe.png",
    difficulty: "Łatwy",
    xpReward: 15,
    goldReward: [10, 25],
  },
  {
    id: "knight",
    name: "Rycerz",
    health: 150,
    damage: [5, 12],
    image: "/knight-foe.png",
    difficulty: "Średni",
    xpReward: 25,
    goldReward: [20, 40],
  },
  {
    id: "orc",
    name: "Ork",
    health: 200,
    damage: [8, 15],
    image: "/orc-foe.png",
    difficulty: "Trudny",
    xpReward: 40,
    goldReward: [30, 60],
  },
]

interface CombatPanelProps {
  playerStats: GameStats
  addExperience: (amount: number) => void
  addGold: (amount: number) => void
  setPlayerHealth: (health: number) => void
}

// Komponent walki
export default function CombatPanel({ playerStats, addExperience, addGold, setPlayerHealth }: CombatPanelProps) {
  const [enemyHealth, setEnemyHealth] = useState(100)
  const [enemyMaxHealth, setEnemyMaxHealth] = useState(100)
  const [combatLog, setCombatLog] = useState<string[]>(["Wchodzisz na arenę...", "Przeciwnik się pojawia!"])
  const [selectedEnemy, setSelectedEnemy] = useState(enemies[0])
  const [inCombat, setInCombat] = useState(false)
  const [combatMode, setCombatMode] = useState<"ai" | "arena">("ai")
  const [attackAnimation, setAttackAnimation] = useState("")
  const [enemyAnimation, setEnemyAnimation] = useState("")
  const [specialAttackCooldown, setSpecialAttackCooldown] = useState(0)

  const playerRef = useRef<HTMLDivElement>(null)
  const enemyRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Efekt dla odliczania cooldownu specjalnego ataku
  useEffect(() => {
    if (specialAttackCooldown > 0) {
      const timer = setTimeout(() => {
        setSpecialAttackCooldown((prev) => prev - 1)
      }, 1000)

      return () => clearTimeout(timer)
    }
  }, [specialAttackCooldown])

  // Rozpoczęcie walki
  const startCombat = () => {
    setEnemyMaxHealth(selectedEnemy.health)
    setEnemyHealth(selectedEnemy.health)
    setPlayerHealth(playerStats.health)
    setCombatLog([`Wchodzisz do walki z przeciwnikiem: ${selectedEnemy.name}`, "Przygotuj się!"])
    setInCombat(true)
    setSpecialAttackCooldown(0)
  }

  // Funkcja do animacji ataku
  const animateAttack = (type: string) => {
    // Animacja gracza
    setAttackAnimation(type)
    setTimeout(() => setAttackAnimation(""), 700)

    // Animacja przeciwnika (z opóźnieniem)
    setTimeout(() => {
      setEnemyAnimation("hit")
      setTimeout(() => setEnemyAnimation(""), 500)
    }, 300)
  }

  // Funkcja do animacji ataku przeciwnika
  const animateEnemyAttack = () => {
    // Animacja przeciwnika
    setEnemyAnimation("attack")
    setTimeout(() => setEnemyAnimation(""), 700)

    // Animacja gracza (z opóźnieniem)
    setTimeout(() => {
      setAttackAnimation("hit")
      setTimeout(() => setAttackAnimation(""), 500)
    }, 300)
  }

  // Atak gracza
  const attack = () => {
    // Obliczanie obrażeń na podstawie siły gracza
    const baseDamage = 5
    const strengthBonus = Math.floor(playerStats.strength / 5)
    const damage = Math.floor(Math.random() * 10) + baseDamage + strengthBonus

    // Animacja ataku
    animateAttack("attack")

    setEnemyHealth((prev) => Math.max(0, prev - damage))
    setCombatLog((prev) => [...prev, `Atakujesz za ${damage} obrażeń!`])

    // Kontratak przeciwnika
    setTimeout(() => {
      if (enemyHealth - damage > 0) {
        enemyAttack()
      } else {
        handleVictory()
      }
    }, 1000)
  }

  // Obrona
  const defend = () => {
    // Animacja obrony
    setAttackAnimation("defend")
    setTimeout(() => setAttackAnimation(""), 700)

    setCombatLog((prev) => [...prev, "Przyjmujesz postawę obronną!"])

    // Atak przeciwnika ze zmniejszonymi obrażeniami
    setTimeout(() => {
      // Animacja ataku przeciwnika
      animateEnemyAttack()

      const minDamage = Math.floor(selectedEnemy.damage[0] / 2)
      const maxDamage = Math.floor(selectedEnemy.damage[1] / 2)
      const defenseBonus = Math.floor(playerStats.defense / 10)
      const enemyDamage = Math.max(
        1,
        Math.floor(Math.random() * (maxDamage - minDamage + 1)) + minDamage - defenseBonus,
      )

      const newHealth = Math.max(0, playerStats.health - enemyDamage)
      setPlayerHealth(newHealth)

      if (newHealth <= 0) {
        handleDefeat()
      } else {
        setCombatLog((prev) => [...prev, `${selectedEnemy.name} atakuje za ${enemyDamage} obrażeń (zredukowane)!`])
      }
    }, 1000)
  }

  // Atak specjalny
  const specialAttack = () => {
    // Obliczanie obrażeń na podstawie siły i zręczności gracza
    const baseDamage = 10
    const strengthBonus = Math.floor(playerStats.strength / 3)
    const agilityBonus = Math.floor(playerStats.agility / 5)
    const damage = Math.floor(Math.random() * 15) + baseDamage + strengthBonus + agilityBonus

    // Animacja ataku specjalnego
    animateAttack("special")

    setEnemyHealth((prev) => Math.max(0, prev - damage))
    setCombatLog((prev) => [...prev, `Wyprowadzasz potężny atak specjalny za ${damage} obrażeń!`])

    // Ustawiamy cooldown na atak specjalny
    setSpecialAttackCooldown(3)

    // Kontratak przeciwnika
    setTimeout(() => {
      if (enemyHealth - damage > 0) {
        enemyAttack()
      } else {
        handleVictory()
      }
    }, 1000)
  }

  // Atak przeciwnika
  const enemyAttack = () => {
    // Animacja ataku przeciwnika
    animateEnemyAttack()

    const minDamage = selectedEnemy.damage[0]
    const maxDamage = selectedEnemy.damage[1]
    const defenseBonus = Math.floor(playerStats.defense / 20)
    const enemyDamage = Math.max(1, Math.floor(Math.random() * (maxDamage - minDamage + 1)) + minDamage - defenseBonus)

    const newHealth = Math.max(0, playerStats.health - enemyDamage)
    setPlayerHealth(newHealth)

    if (newHealth <= 0) {
      handleDefeat()
    } else {
      setCombatLog((prev) => [...prev, `${selectedEnemy.name} atakuje za ${enemyDamage} obrażeń!`])
    }
  }

  // Obsługa zwycięstwa
  const handleVictory = () => {
    // Obliczanie nagród
    const xpReward = selectedEnemy.xpReward
    const minGold = selectedEnemy.goldReward[0]
    const maxGold = selectedEnemy.goldReward[1]
    const goldReward = Math.floor(Math.random() * (maxGold - minGold + 1)) + minGold

    // Dodawanie nagród
    addExperience(xpReward)
    addGold(goldReward)

    // Aktualizacja dziennika walki
    setCombatLog((prev) => [
      ...prev,
      `Pokonałeś przeciwnika: ${selectedEnemy.name}!`,
      `Otrzymujesz ${xpReward} PD i ${goldReward} złota!`,
    ])

    // Wyświetlanie toastu z informacją o nagrodach
    toast({
      title: "Zwycięstwo!",
      description: `Pokonałeś ${selectedEnemy.name}! Otrzymujesz ${xpReward} PD i ${goldReward} złota.`,
      variant: "default",
    })

    setInCombat(false)
  }

  // Obsługa porażki
  const handleDefeat = () => {
    setCombatLog((prev) => [...prev, `${selectedEnemy.name} zadaje ci śmiertelny cios!`, "Zostałeś pokonany!"])

    toast({
      title: "Porażka!",
      description: `Zostałeś pokonany przez ${selectedEnemy.name}!`,
      variant: "destructive",
    })

    setInCombat(false)
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6">
      <Tabs defaultValue="ai" onValueChange={(value) => setCombatMode(value as "ai" | "arena")}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Arena Walki</h2>
          <TabsList className="bg-slate-700">
            <TabsTrigger value="ai" className="data-[state=active]:bg-slate-600">
              <Bot className="h-4 w-4 mr-2" />
              Boty AI
            </TabsTrigger>
            <TabsTrigger value="arena" className="data-[state=active]:bg-slate-600">
              <User className="h-4 w-4 mr-2" />
              Arena PvP
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="ai" className="mt-0">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              {!inCombat ? (
                <div className="bg-slate-700 rounded-lg p-6 mb-6">
                  <h3 className="font-bold mb-4">Wybierz przeciwnika</h3>
                  <div className="mb-4">
                    <Select
                      onValueChange={(value) => setSelectedEnemy(enemies.find((e) => e.id === value) || enemies[0])}
                      defaultValue={selectedEnemy.id}
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Wybierz przeciwnika" />
                      </SelectTrigger>
                      <SelectContent>
                        {enemies.map((enemy) => (
                          <SelectItem key={enemy.id} value={enemy.id}>
                            {enemy.name} - {enemy.difficulty}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center gap-4 mb-6">
                    <img
                      src={selectedEnemy.image || "/placeholder.svg"}
                      alt={selectedEnemy.name}
                      className="h-16 w-16 rounded-full bg-slate-800"
                    />
                    <div>
                      <h4 className="font-bold">{selectedEnemy.name}</h4>
                      <p className="text-sm text-gray-400">Poziom trudności: {selectedEnemy.difficulty}</p>
                      <p className="text-sm">Zdrowie: {selectedEnemy.health}</p>
                      <p className="text-sm">
                        Nagroda: {selectedEnemy.xpReward} PD, {selectedEnemy.goldReward[0]}-
                        {selectedEnemy.goldReward[1]} złota
                      </p>
                    </div>
                  </div>

                  <Button onClick={startCombat} className="w-full">
                    Rozpocznij walkę
                  </Button>
                </div>
              ) : (
                <>
                  <div className="bg-slate-700 rounded-lg p-4 mb-4 relative overflow-hidden">
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center gap-2">
                        <div
                          ref={playerRef}
                          className={`relative ${
                            attackAnimation === "attack"
                              ? "animate-player-attack"
                              : attackAnimation === "special"
                                ? "animate-player-special"
                                : attackAnimation === "defend"
                                  ? "animate-player-defend"
                                  : attackAnimation === "hit"
                                    ? "animate-player-hit"
                                    : ""
                          }`}
                        >
                          <img src="/stoic-elf-guardian.png" alt="Gracz" className="h-16 w-16 rounded-full" />
                          {attackAnimation === "defend" && (
                            <div className="absolute inset-0 rounded-full border-4 border-blue-400 animate-pulse"></div>
                          )}
                          {attackAnimation === "special" && (
                            <div className="absolute -inset-2 rounded-full border-2 border-yellow-400 animate-spin"></div>
                          )}
                        </div>
                        <span>Ty</span>
                      </div>
                      <span>
                        {playerStats.health}/{playerStats.maxHealth}
                      </span>
                    </div>
                    <Progress value={(playerStats.health / playerStats.maxHealth) * 100} className="h-2" />
                  </div>

                  <div className="bg-slate-700 rounded-lg p-4 mb-6 relative overflow-hidden">
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center gap-2">
                        <div
                          ref={enemyRef}
                          className={`relative ${
                            enemyAnimation === "attack"
                              ? "animate-enemy-attack"
                              : enemyAnimation === "hit"
                                ? "animate-enemy-hit"
                                : ""
                          }`}
                        >
                          <img
                            src={selectedEnemy.image || "/placeholder.svg"}
                            alt={selectedEnemy.name}
                            className="h-16 w-16 rounded-full"
                          />
                          {enemyAnimation === "hit" && (
                            <div className="absolute inset-0 bg-red-500 rounded-full opacity-40 animate-pulse"></div>
                          )}
                        </div>
                        <span>{selectedEnemy.name}</span>
                      </div>
                      <span>
                        {enemyHealth}/{enemyMaxHealth}
                      </span>
                    </div>
                    <Progress
                      value={(enemyHealth / enemyMaxHealth) * 100}
                      className="h-2"
                      indicatorClassName="bg-red-500"
                    />

                    {/* Efekty wizualne walki */}
                    <div className="absolute inset-0 pointer-events-none">
                      {attackAnimation === "attack" && (
                        <div className="absolute top-1/2 left-1/2 w-8 h-8 bg-red-500 rounded-full opacity-0 animate-hit-effect"></div>
                      )}
                      {attackAnimation === "special" && (
                        <div className="absolute top-1/2 left-1/2 w-12 h-12 bg-yellow-500 rounded-full opacity-0 animate-special-effect"></div>
                      )}
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-3">
                    <Button onClick={attack} className="flex-1 bg-red-600 hover:bg-red-700" disabled={!inCombat}>
                      <Sword className="h-4 w-4 mr-2" />
                      Atak
                    </Button>
                    <Button onClick={defend} variant="outline" className="flex-1" disabled={!inCombat}>
                      <Shield className="h-4 w-4 mr-2" />
                      Obrona
                    </Button>
                    <Button
                      onClick={specialAttack}
                      className="flex-1 bg-purple-600 hover:bg-purple-700"
                      disabled={!inCombat || specialAttackCooldown > 0}
                    >
                      <Zap className="h-4 w-4 mr-2" />
                      Specjalny {specialAttackCooldown > 0 && `(${specialAttackCooldown}s)`}
                    </Button>
                  </div>
                </>
              )}
            </div>

            <div>
              <div className="bg-slate-700 rounded-lg p-4 h-full">
                <h3 className="font-semibold mb-3 text-gray-300">Dziennik Walki</h3>
                <div className="space-y-2 h-[300px] overflow-y-auto text-sm">
                  {combatLog.map((log, index) => (
                    <div key={index} className="text-gray-300 border-l-2 border-gray-600 pl-2">
                      {log}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="arena" className="mt-0">
          <div className="bg-slate-700 rounded-lg p-6">
            <h3 className="font-bold mb-4">Arena PvP</h3>
            <p className="text-gray-300 mb-6">
              Walcz z innymi graczami i zdobywaj nagrody! Wygraj wystarczająco dużo walk, aby awansować w rankingu.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="bg-slate-800 p-4 rounded-lg">
                <h4 className="font-bold text-yellow-400 mb-2">Ranking Areny</h4>
                <ul className="space-y-2">
                  {["MistrzMiecza", "ZabójcaSmoków", "KrólRycerzy", "TancerzOstrzy", "NosicielTarczy"].map(
                    (name, index) => (
                      <li key={index} className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <span className="text-gray-400">{index + 1}.</span>
                          <span>{name}</span>
                        </div>
                        <span className="text-gray-400">Zwycięstwa: {Math.floor(Math.random() * 50) + 20}</span>
                      </li>
                    ),
                  )}
                </ul>
              </div>

              <div className="bg-slate-800 p-4 rounded-lg">
                <h4 className="font-bold text-yellow-400 mb-2">Nagrody Areny</h4>
                <ul className="space-y-2">
                  <li className="flex justify-between items-center">
                    <span>5 zwycięstw</span>
                    <span className="text-gray-400">100 złota</span>
                  </li>
                  <li className="flex justify-between items-center">
                    <span>10 zwycięstw</span>
                    <span className="text-gray-400">Rzadki przedmiot</span>
                  </li>
                  <li className="flex justify-between items-center">
                    <span>25 zwycięstw</span>
                    <span className="text-gray-400">Tytuł "Mistrz Areny"</span>
                  </li>
                  <li className="flex justify-between items-center">
                    <span>50 zwycięstw</span>
                    <span className="text-gray-400">Legendarny miecz</span>
                  </li>
                </ul>
              </div>
            </div>

            <Button className="w-full">Znajdź przeciwnika</Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
