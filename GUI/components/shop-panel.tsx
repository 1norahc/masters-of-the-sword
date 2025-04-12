"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Sword, Shield, FlaskRoundIcon as Flask, HardDriveIcon as Boot, Shirt } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

// Typy przedmiotów
type ItemCategory = "weapon" | "armor" | "potion" | "accessory"

interface ShopItem {
  id: number
  name: string
  description: string
  price: number
  category: ItemCategory
  stats: string
  icon: any
  requiredLevel: number
}

interface ShopPanelProps {
  gold: number
  spendGold: (amount: number) => boolean
  level: number
}

export default function ShopPanel({ gold, spendGold, level }: ShopPanelProps) {
  const { toast } = useToast()

  // Lista przedmiotów w sklepie
  const shopItems: ShopItem[] = [
    // Broń
    {
      id: 1,
      name: "Żelazny Miecz",
      description: "Podstawowy miecz wykonany z żelaza.",
      price: 100,
      category: "weapon",
      stats: "+8 Atak",
      icon: Sword,
      requiredLevel: 1,
    },
    {
      id: 2,
      name: "Stalowy Miecz",
      description: "Solidny miecz ze stali.",
      price: 250,
      category: "weapon",
      stats: "+15 Atak",
      icon: Sword,
      requiredLevel: 3,
    },
    {
      id: 3,
      name: "Miecz z Mithrilu",
      description: "Rzadki miecz wykonany z mithrilu.",
      price: 500,
      category: "weapon",
      stats: "+25 Atak",
      icon: Sword,
      requiredLevel: 5,
    },

    // Zbroja
    {
      id: 4,
      name: "Skórzana Zbroja",
      description: "Podstawowa zbroja ze skóry.",
      price: 80,
      category: "armor",
      stats: "+5 Obrona",
      icon: Shirt,
      requiredLevel: 1,
    },
    {
      id: 5,
      name: "Kolczuga",
      description: "Solidna zbroja z metalowych ogniw.",
      price: 200,
      category: "armor",
      stats: "+12 Obrona",
      icon: Shirt,
      requiredLevel: 2,
    },
    {
      id: 6,
      name: "Płytowa Zbroja",
      description: "Ciężka zbroja z metalowych płyt.",
      price: 450,
      category: "armor",
      stats: "+20 Obrona",
      icon: Shirt,
      requiredLevel: 4,
    },

    // Mikstury
    {
      id: 7,
      name: "Mała Mikstura Zdrowia",
      description: "Przywraca 20 punktów zdrowia.",
      price: 25,
      category: "potion",
      stats: "+20 Zdrowie",
      icon: Flask,
      requiredLevel: 1,
    },
    {
      id: 8,
      name: "Duża Mikstura Zdrowia",
      description: "Przywraca 50 punktów zdrowia.",
      price: 60,
      category: "potion",
      stats: "+50 Zdrowie",
      icon: Flask,
      requiredLevel: 1,
    },
    {
      id: 9,
      name: "Mikstura Energii",
      description: "Przywraca 30 punktów energii.",
      price: 40,
      category: "potion",
      stats: "+30 Energia",
      icon: Flask,
      requiredLevel: 1,
    },

    // Akcesoria
    {
      id: 10,
      name: "Skórzane Buty",
      description: "Podstawowe buty ze skóry.",
      price: 50,
      category: "accessory",
      stats: "+3 Zręczność",
      icon: Boot,
      requiredLevel: 1,
    },
    {
      id: 11,
      name: "Stalowa Tarcza",
      description: "Solidna tarcza ze stali.",
      price: 150,
      category: "accessory",
      stats: "+10 Obrona",
      icon: Shield,
      requiredLevel: 2,
    },
    {
      id: 12,
      name: "Amulet Siły",
      description: "Zwiększa siłę właściciela.",
      price: 300,
      category: "accessory",
      stats: "+8 Siła",
      icon: Shield,
      requiredLevel: 3,
    },
  ]

  const [activeCategory, setActiveCategory] = useState<ItemCategory>("weapon")
  const [cart, setCart] = useState<number[]>([])

  // Filtrowanie przedmiotów według kategorii
  const filteredItems = shopItems.filter((item) => item.category === activeCategory)

  // Obliczanie całkowitej ceny koszyka
  const totalPrice = cart.reduce((total, itemId) => {
    const item = shopItems.find((i) => i.id === itemId)
    return total + (item?.price || 0)
  }, 0)

  // Dodawanie przedmiotu do koszyka
  const addToCart = (itemId: number) => {
    setCart([...cart, itemId])
  }

  // Usuwanie przedmiotu z koszyka
  const removeFromCart = (itemId: number) => {
    const index = cart.indexOf(itemId)
    if (index !== -1) {
      const newCart = [...cart]
      newCart.splice(index, 1)
      setCart(newCart)
    }
  }

  // Zakup przedmiotów
  const purchaseItems = () => {
    if (cart.length === 0) {
      toast({
        title: "Koszyk jest pusty",
        description: "Dodaj przedmioty do koszyka przed zakupem.",
        variant: "destructive",
      })
      return
    }

    // Sprawdzamy czy gracz ma wystarczająco złota
    if (spendGold(totalPrice)) {
      toast({
        title: "Zakup udany!",
        description: `Zakupiono ${cart.length} przedmiotów za ${totalPrice} złota.`,
        variant: "default",
      })

      // Czyszczenie koszyka po zakupie
      setCart([])
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Sklep</h2>
        <div className="flex items-center gap-2">
          <span className="text-gray-300">Złoto:</span>
          <span className="font-bold text-yellow-400">{gold}</span>
        </div>
      </div>

      <Tabs defaultValue="weapon" onValueChange={(value) => setActiveCategory(value as ItemCategory)}>
        <TabsList className="grid grid-cols-4 bg-slate-700">
          <TabsTrigger value="weapon" className="data-[state=active]:bg-slate-600">
            <Sword className="h-4 w-4 mr-2" />
            Broń
          </TabsTrigger>
          <TabsTrigger value="armor" className="data-[state=active]:bg-slate-600">
            <Shirt className="h-4 w-4 mr-2" />
            Zbroja
          </TabsTrigger>
          <TabsTrigger value="potion" className="data-[state=active]:bg-slate-600">
            <Flask className="h-4 w-4 mr-2" />
            Mikstury
          </TabsTrigger>
          <TabsTrigger value="accessory" className="data-[state=active]:bg-slate-600">
            <Shield className="h-4 w-4 mr-2" />
            Akcesoria
          </TabsTrigger>
        </TabsList>

        <div className="mt-4 flex-1 overflow-y-auto">
          <div className="space-y-3 mb-6">
            {filteredItems.map((item) => (
              <div key={item.id} className="bg-slate-700 p-3 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 bg-slate-600 rounded-md flex items-center justify-center">
                    <item.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <div className="font-medium">{item.name}</div>
                      <div className="text-yellow-400">{item.price} złota</div>
                    </div>
                    <div className="text-xs text-gray-400">{item.description}</div>
                    <div className="text-xs text-green-400">{item.stats}</div>
                    {item.requiredLevel > level && (
                      <div className="text-xs text-red-400">Wymagany poziom: {item.requiredLevel}</div>
                    )}
                  </div>
                </div>
                <div className="mt-2 flex justify-end">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => addToCart(item.id)}
                    disabled={item.requiredLevel > level || cart.includes(item.id)}
                  >
                    {cart.includes(item.id) ? "W koszyku" : "Dodaj do koszyka"}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Tabs>

      {/* Koszyk */}
      <div className="mt-auto">
        <div className="bg-slate-700 p-3 rounded-lg">
          <h3 className="font-bold mb-2">Koszyk ({cart.length})</h3>

          {cart.length > 0 ? (
            <div className="space-y-2 max-h-40 overflow-y-auto mb-3">
              {cart.map((itemId) => {
                const item = shopItems.find((i) => i.id === itemId)
                if (!item) return null

                return (
                  <div key={itemId} className="flex justify-between items-center bg-slate-600 p-2 rounded">
                    <div className="flex items-center gap-2">
                      <item.icon className="h-4 w-4" />
                      <span className="text-sm">{item.name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-yellow-400">{item.price}</span>
                      <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => removeFromCart(itemId)}>
                        ×
                      </Button>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="text-sm text-gray-400 mb-3">Koszyk jest pusty</div>
          )}

          <div className="flex justify-between items-center mb-3">
            <span>Suma:</span>
            <span className="font-bold text-yellow-400">{totalPrice} złota</span>
          </div>

          <Button className="w-full" onClick={purchaseItems} disabled={cart.length === 0 || totalPrice > gold}>
            Kup teraz
          </Button>
        </div>
      </div>
    </div>
  )
}
