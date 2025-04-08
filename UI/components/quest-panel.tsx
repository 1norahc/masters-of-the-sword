import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Clock, Skull, Coins } from "lucide-react"

type Quest = {
  id: number
  title: string
  description: string
  difficulty: "easy" | "medium" | "hard" | "epic"
  duration: number // in minutes
  rewards: {
    gold: number
    experience: number
    items?: string[]
  }
}

export default function QuestPanel() {
  const quests: Quest[] = [
    {
      id: 1,
      title: "Goblin Trouble",
      description: "Clear out the goblins that have been causing trouble for local farmers.",
      difficulty: "easy",
      duration: 15,
      rewards: {
        gold: 150,
        experience: 50,
      },
    },
    {
      id: 2,
      title: "Missing Shipment",
      description: "Find the merchant's missing shipment that was ambushed on the road.",
      difficulty: "medium",
      duration: 30,
      rewards: {
        gold: 300,
        experience: 100,
        items: ["Health Potion"],
      },
    },
    {
      id: 3,
      title: "Dragon's Hoard",
      description: "Brave the dragon's lair and steal a portion of its legendary treasure.",
      difficulty: "hard",
      duration: 60,
      rewards: {
        gold: 800,
        experience: 250,
        items: ["Dragon Scale", "Gold Ring"],
      },
    },
    {
      id: 4,
      title: "The Ancient Evil",
      description: "Venture into the forbidden temple and defeat the ancient evil that lurks within.",
      difficulty: "epic",
      duration: 120,
      rewards: {
        gold: 2000,
        experience: 500,
        items: ["Legendary Sword", "Magic Amulet"],
      },
    },
  ]

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "easy":
        return "bg-green-700"
      case "medium":
        return "bg-yellow-700"
      case "hard":
        return "bg-red-700"
      case "epic":
        return "bg-purple-700"
      default:
        return "bg-slate-700"
    }
  }

  return (
    <div className="space-y-4">
      {quests.map((quest) => (
        <Card key={quest.id} className="bg-slate-800/60 border-slate-700">
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <div>
                <CardTitle>{quest.title}</CardTitle>
                <CardDescription className="text-slate-300">{quest.description}</CardDescription>
              </div>
              <div className={`${getDifficultyColor(quest.difficulty)} px-2 py-1 rounded text-xs font-bold uppercase`}>
                {quest.difficulty}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center gap-1 text-sm">
                <Clock className="h-4 w-4 text-slate-400" />
                <span>{quest.duration} min</span>
              </div>
              <div className="flex items-center gap-1 text-sm">
                <Skull className="h-4 w-4 text-slate-400" />
                <span>
                  Enemies:{" "}
                  {quest.difficulty === "easy"
                    ? "Weak"
                    : quest.difficulty === "medium"
                      ? "Strong"
                      : quest.difficulty === "hard"
                        ? "Elite"
                        : "Boss"}
                </span>
              </div>
            </div>

            <div className="bg-slate-700/40 rounded-md p-3 mb-4">
              <h4 className="text-sm font-semibold mb-2">Rewards:</h4>
              <div className="flex flex-wrap gap-3">
                <div className="flex items-center gap-1">
                  <Coins className="h-4 w-4 text-yellow-400" />
                  <span className="text-yellow-400">{quest.rewards.gold} gold</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="h-4 w-4 rounded-full bg-blue-400 flex items-center justify-center text-xs font-bold">
                    XP
                  </div>
                  <span className="text-blue-400">{quest.rewards.experience} XP</span>
                </div>
                {quest.rewards.items &&
                  quest.rewards.items.map((item, index) => (
                    <div key={index} className="text-purple-400 text-sm">
                      +{item}
                    </div>
                  ))}
              </div>
            </div>

            <Button className="w-full bg-amber-700 hover:bg-amber-600">Start Quest</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
