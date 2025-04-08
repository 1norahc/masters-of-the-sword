"use client"

import { useState } from "react"
import { Sword, Shield, PillBottleIcon as Potion, Coins, Award, Users, Map, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import CharacterCard from "@/components/character-card"
import GameMenu from "@/components/game-menu"
import InventoryPanel from "@/components/inventory-panel"
import QuestPanel from "@/components/quest-panel"

export default function GameInterface() {
  const [gold, setGold] = useState(1250)
  const [level, setLevel] = useState(12)
  const [experience, setExperience] = useState(75)

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-purple-950 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-2">
            <h1 className="text-3xl font-extrabold text-yellow-400 drop-shadow-[0_2px_2px_rgba(0,0,0,0.8)]">
              Masters Of The Sword
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1 bg-yellow-900/60 px-3 py-1 rounded-full">
              <Coins className="h-5 w-5 text-yellow-400" />
              <span className="font-bold text-yellow-400">{gold}</span>
            </div>
            <Button variant="outline" size="icon" className="bg-red-900/60 border-red-700 hover:bg-red-800">
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left sidebar - Character */}
          <div className="lg:col-span-3">
            <CharacterCard />

            <Card className="mt-4 bg-slate-800/60 border-slate-700">
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Stats</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Level {level}</span>
                      <span>XP: {experience}/100</span>
                    </div>
                    <Progress value={experience} className="h-2 bg-slate-700" />
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div className="flex items-center gap-2">
                      <Sword className="h-4 w-4 text-red-400" />
                      <span>Strength: 42</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4 text-blue-400" />
                      <span>Defense: 38</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Potion className="h-4 w-4 text-green-400" />
                      <span>Health: 320</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Award className="h-4 w-4 text-yellow-400" />
                      <span>Luck: 15</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Center - Main game area */}
          <div className="lg:col-span-6">
            <Tabs defaultValue="quests" className="w-full">
              <TabsList className="grid grid-cols-4 bg-slate-800/60">
                <TabsTrigger value="quests" className="data-[state=active]:bg-purple-700">
                  Quests
                </TabsTrigger>
                <TabsTrigger value="dungeon" className="data-[state=active]:bg-purple-700">
                  Dungeon
                </TabsTrigger>
                <TabsTrigger value="arena" className="data-[state=active]:bg-purple-700">
                  Arena
                </TabsTrigger>
                <TabsTrigger value="tavern" className="data-[state=active]:bg-purple-700">
                  Tavern
                </TabsTrigger>
              </TabsList>
              <TabsContent value="quests" className="mt-4">
                <QuestPanel />
              </TabsContent>
              <TabsContent value="dungeon" className="mt-4">
                <Card className="bg-slate-800/60 border-slate-700">
                  <CardHeader>
                    <CardTitle>Dungeon Adventures</CardTitle>
                    <CardDescription className="text-slate-300">
                      Explore dangerous dungeons for rare loot
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-col items-center justify-center p-8 text-center">
                      <Map className="h-16 w-16 mb-4 text-amber-400" />
                      <p className="mb-4">Choose a dungeon to explore</p>
                      <div className="grid grid-cols-2 gap-4 w-full">
                        <Button className="bg-amber-700 hover:bg-amber-600">Goblin Caves</Button>
                        <Button className="bg-amber-700 hover:bg-amber-600">Haunted Mines</Button>
                        <Button className="bg-amber-700 hover:bg-amber-600">Dragon's Lair</Button>
                        <Button className="bg-amber-700 hover:bg-amber-600">Cursed Temple</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="arena" className="mt-4">
                <Card className="bg-slate-800/60 border-slate-700">
                  <CardHeader>
                    <CardTitle>Arena Battles</CardTitle>
                    <CardDescription className="text-slate-300">
                      Fight other players for glory and rewards
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-col items-center justify-center p-8 text-center">
                      <Users className="h-16 w-16 mb-4 text-red-400" />
                      <p className="mb-4">Find opponents to battle</p>
                      <Button className="bg-red-700 hover:bg-red-600 w-full mb-4">Find Opponent</Button>
                      <div className="w-full bg-slate-700/60 rounded-md p-4">
                        <p className="text-sm text-slate-300">Arena rank: #156</p>
                        <p className="text-sm text-slate-300">Wins: 24 | Losses: 18</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="tavern" className="mt-4">
                <Card className="bg-slate-800/60 border-slate-700">
                  <CardHeader>
                    <CardTitle>Tavern</CardTitle>
                    <CardDescription className="text-slate-300">Relax, drink, and find new quests</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-col items-center justify-center p-8 text-center">
                      <Potion className="h-16 w-16 mb-4 text-green-400" />
                      <p className="mb-4">The tavern is full of interesting characters...</p>
                      <div className="grid grid-cols-2 gap-4 w-full">
                        <Button className="bg-green-700 hover:bg-green-600">Talk to Bartender</Button>
                        <Button className="bg-green-700 hover:bg-green-600">Play Dice Game</Button>
                        <Button className="bg-green-700 hover:bg-green-600">Buy Drinks</Button>
                        <Button className="bg-green-700 hover:bg-green-600">Listen to Rumors</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Right sidebar - Inventory */}
          <div className="lg:col-span-3">
            <GameMenu />
            <InventoryPanel />
          </div>
        </div>
      </div>
    </div>
  )
}
