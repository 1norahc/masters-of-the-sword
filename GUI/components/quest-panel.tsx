"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Scroll, Coins, Swords } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface QuestPanelProps {
  addExperience: (amount: number) => void
  addGold: (amount: number) => void
}

export default function QuestPanel({ addExperience, addGold }: QuestPanelProps) {
  const { toast } = useToast()
  const [quests, setQuests] = useState([
    {
      id: 1,
      title: "Obóz Bandytów",
      description: "Oczyść obóz bandytów znajdujący się za murami miasta.",
      reward: "50 Złota, 20 PD",
      difficulty: "Łatwe",
      progress: 0,
      total: 5,
      status: "available",
      xpReward: 20,
      goldReward: 50,
    },
    {
      id: 2,
      title: "Mistrz Areny",
      description: "Wygraj 3 walki z rzędu na arenie.",
      reward: "100 Złota, 40 PD",
      difficulty: "Średnie",
      progress: 1,
      total: 3,
      status: "in-progress",
      xpReward: 40,
      goldReward: 100,
    },
    {
      id: 3,
      title: "Zaginiony Miecz",
      description: "Znajdź legendarny miecz ukryty w starożytnych ruinach.",
      reward: "200 Złota, 60 PD, Rzadki Miecz",
      difficulty: "Trudne",
      progress: 0,
      total: 1,
      status: "available",
      xpReward: 60,
      goldReward: 200,
    },
  ])

  const acceptQuest = (id: number) => {
    setQuests(quests.map((quest) => (quest.id === id ? { ...quest, status: "in-progress" } : quest)))

    toast({
      title: "Zadanie przyjęte",
      description: "Możesz teraz rozpocząć wykonywanie zadania.",
      variant: "default",
    })
  }

  const progressQuest = (id: number) => {
    setQuests(
      quests.map((quest) => {
        if (quest.id === id && quest.status === "in-progress") {
          const newProgress = quest.progress + 1

          // Sprawdzamy czy zadanie zostało ukończone
          if (newProgress >= quest.total) {
            // Przyznajemy nagrody
            addExperience(quest.xpReward)
            addGold(quest.goldReward)

            toast({
              title: "Zadanie ukończone!",
              description: `Otrzymujesz ${quest.xpReward} PD i ${quest.goldReward} złota.`,
              variant: "default",
            })

            // Oznaczamy zadanie jako ukończone
            return { ...quest, status: "completed", progress: quest.total }
          }

          // Aktualizujemy postęp
          return { ...quest, progress: newProgress }
        }
        return quest
      }),
    )
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Zadania</h2>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            Codzienne
          </Button>
          <Button variant="outline" size="sm">
            Gildia
          </Button>
        </div>
      </div>

      <div className="space-y-4">
        {quests
          .filter((quest) => quest.status !== "completed")
          .map((quest) => (
            <div key={quest.id} className="bg-slate-700 p-4 rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{quest.title}</h3>
                <div
                  className={`text-xs px-2 py-1 rounded ${
                    quest.difficulty === "Łatwe"
                      ? "bg-green-900 text-green-300"
                      : quest.difficulty === "Średnie"
                        ? "bg-yellow-900 text-yellow-300"
                        : "bg-red-900 text-red-300"
                  }`}
                >
                  {quest.difficulty}
                </div>
              </div>

              <p className="text-gray-300 text-sm mb-3">{quest.description}</p>

              <div className="flex items-center gap-2 text-sm text-gray-400 mb-3">
                <Coins className="h-4 w-4 text-yellow-400" />
                <span>Nagroda: {quest.reward}</span>
              </div>

              {quest.status === "in-progress" && (
                <div className="mb-3">
                  <div className="flex justify-between text-xs mb-1">
                    <span>Postęp</span>
                    <span>
                      {quest.progress}/{quest.total}
                    </span>
                  </div>
                  <Progress value={(quest.progress / quest.total) * 100} className="h-2" />
                </div>
              )}

              <div className="flex justify-end">
                {quest.status === "available" ? (
                  <Button onClick={() => acceptQuest(quest.id)}>
                    <Scroll className="h-4 w-4 mr-2" />
                    Przyjmij
                  </Button>
                ) : (
                  <Button variant="outline" onClick={() => progressQuest(quest.id)}>
                    <Swords className="h-4 w-4 mr-2" />
                    Kontynuuj
                  </Button>
                )}
              </div>
            </div>
          ))}
      </div>
    </div>
  )
}
