"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sword, Shield, Shirt, BellRingIcon as Ring, Scroll } from "lucide-react"

type InventoryItem = {
  id: number
  name: string
  type: string
  stats: string
  rarity: "common" | "uncommon" | "rare" | "epic" | "legendary"
  equipped?: boolean
}

export default function InventoryPanel() {
  const [items, setItems] = useState<InventoryItem[]>([
    { id: 1, name: "Steel Sword", type: "weapon", stats: "+12 Strength", rarity: "uncommon", equipped: true },
    { id: 2, name: "Iron Shield", type: "shield", stats: "+10 Defense", rarity: "common", equipped: true },
    { id: 3, name: "Leather Armor", type: "armor", stats: "+8 Defense", rarity: "common", equipped: true },
    { id: 4, name: "Lucky Ring", type: "accessory", stats: "+5 Luck", rarity: "rare", equipped: true },
    { id: 5, name: "Rusty Dagger", type: "weapon", stats: "+5 Strength", rarity: "common" },
    { id: 6, name: "Wooden Shield", type: "shield", stats: "+4 Defense", rarity: "common" },
    { id: 7, name: "Magic Scroll", type: "consumable", stats: "Restores 50 Mana", rarity: "uncommon" },
    { id: 8, name: "Health Potion", type: "consumable", stats: "Restores 100 Health", rarity: "common" },
  ])

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case "common":
        return "text-slate-200"
      case "uncommon":
        return "text-green-400"
      case "rare":
        return "text-blue-400"
      case "epic":
        return "text-purple-400"
      case "legendary":
        return "text-orange-400"
      default:
        return "text-slate-200"
    }
  }

  const getItemIcon = (type: string) => {
    switch (type) {
      case "weapon":
        return <Sword className="h-4 w-4" />
      case "shield":
        return <Shield className="h-4 w-4" />
      case "armor":
        return <Shirt className="h-4 w-4" />
      case "accessory":
        return <Ring className="h-4 w-4" />
      case "consumable":
        return <Scroll className="h-4 w-4" />
      default:
        return <Sword className="h-4 w-4" />
    }
  }

  return (
    <Card className="bg-slate-800/60 border-slate-700">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Inventory</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="all">
          <TabsList className="grid grid-cols-4 bg-slate-700/60">
            <TabsTrigger value="all" className="text-xs">
              All
            </TabsTrigger>
            <TabsTrigger value="equipment" className="text-xs">
              Equipment
            </TabsTrigger>
            <TabsTrigger value="consumables" className="text-xs">
              Consumables
            </TabsTrigger>
            <TabsTrigger value="equipped" className="text-xs">
              Equipped
            </TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-2">
            <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
              {items.map((item) => (
                <div
                  key={item.id}
                  className={`flex items-center p-2 rounded-md ${item.equipped ? "bg-slate-700/80" : "bg-slate-700/40 hover:bg-slate-700/60"} cursor-pointer`}
                >
                  <div className="mr-2">{getItemIcon(item.type)}</div>
                  <div className="flex-1">
                    <div className={`font-medium ${getRarityColor(item.rarity)}`}>{item.name}</div>
                    <div className="text-xs text-slate-400">{item.stats}</div>
                  </div>
                  {item.equipped && <div className="text-xs bg-green-800 px-1.5 py-0.5 rounded">Equipped</div>}
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="equipment" className="mt-2">
            <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
              {items
                .filter((item) => ["weapon", "shield", "armor", "accessory"].includes(item.type))
                .map((item) => (
                  <div
                    key={item.id}
                    className={`flex items-center p-2 rounded-md ${item.equipped ? "bg-slate-700/80" : "bg-slate-700/40 hover:bg-slate-700/60"} cursor-pointer`}
                  >
                    <div className="mr-2">{getItemIcon(item.type)}</div>
                    <div className="flex-1">
                      <div className={`font-medium ${getRarityColor(item.rarity)}`}>{item.name}</div>
                      <div className="text-xs text-slate-400">{item.stats}</div>
                    </div>
                    {item.equipped && <div className="text-xs bg-green-800 px-1.5 py-0.5 rounded">Equipped</div>}
                  </div>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="consumables" className="mt-2">
            <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
              {items
                .filter((item) => item.type === "consumable")
                .map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center p-2 rounded-md bg-slate-700/40 hover:bg-slate-700/60 cursor-pointer"
                  >
                    <div className="mr-2">{getItemIcon(item.type)}</div>
                    <div className="flex-1">
                      <div className={`font-medium ${getRarityColor(item.rarity)}`}>{item.name}</div>
                      <div className="text-xs text-slate-400">{item.stats}</div>
                    </div>
                  </div>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="equipped" className="mt-2">
            <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1">
              {items
                .filter((item) => item.equipped)
                .map((item) => (
                  <div key={item.id} className="flex items-center p-2 rounded-md bg-slate-700/80 cursor-pointer">
                    <div className="mr-2">{getItemIcon(item.type)}</div>
                    <div className="flex-1">
                      <div className={`font-medium ${getRarityColor(item.rarity)}`}>{item.name}</div>
                      <div className="text-xs text-slate-400">{item.stats}</div>
                    </div>
                    <div className="text-xs bg-green-800 px-1.5 py-0.5 rounded">Equipped</div>
                  </div>
                ))}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
