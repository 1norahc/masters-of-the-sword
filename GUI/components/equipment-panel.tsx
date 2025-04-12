"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Sword, Shield, HardDriveIcon as Boot, Shirt } from "lucide-react"
import { DndProvider, useDrag, useDrop } from "react-dnd"
import { HTML5Backend } from "react-dnd-html5-backend"

// Typ przedmiotu
type ItemType = {
  id: number
  name: string
  type: string
  stats: string
  equipped: boolean
  icon: any
}

// Komponent przedmiotu z możliwością przeciągania
const DraggableItem = ({
  item,
  onEquip,
  onUnequip,
  isEquipped,
}: {
  item: ItemType
  onEquip: (id: number) => void
  onUnequip: (id: number) => void
  isEquipped: boolean
}) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "ITEM",
    item: { id: item.id },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }))

  return (
    <div
      ref={drag}
      className={`flex items-center bg-slate-700 p-3 rounded-lg ${isDragging ? "opacity-50" : "opacity-100"}`}
    >
      <div className="h-10 w-10 bg-slate-600 rounded-md flex items-center justify-center mr-3">
        <item.icon className="h-6 w-6" />
      </div>
      <div className="flex-1">
        <div className="font-medium">{item.name}</div>
        <div className="text-xs text-gray-400">{item.stats}</div>
      </div>
      {isEquipped ? (
        <Button variant="ghost" size="sm" onClick={() => onUnequip(item.id)}>
          Zdejmij
        </Button>
      ) : (
        <Button variant="outline" size="sm" onClick={() => onEquip(item.id)}>
          Załóż
        </Button>
      )}
    </div>
  )
}

// Obszar do upuszczania przedmiotów
const DropArea = ({
  onDrop,
  children,
  title,
}: {
  onDrop: (id: number) => void
  children: React.ReactNode
  title: string
}) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: "ITEM",
    drop: (item: { id: number }) => {
      onDrop(item.id)
      return undefined
    },
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }))

  return (
    <div>
      <h3 className="text-lg font-semibold mb-3 text-gray-300">{title}</h3>
      <div ref={drop} className={`space-y-3 p-2 rounded-lg ${isOver ? "bg-slate-600/50" : ""}`}>
        {children}
      </div>
    </div>
  )
}

export default function EquipmentPanel() {
  const [items, setItems] = useState<ItemType[]>([
    { id: 1, name: "Zardzewiały Miecz", type: "weapon", stats: "+5 Atak", equipped: true, icon: Sword },
    { id: 2, name: "Drewniana Tarcza", type: "shield", stats: "+3 Obrona", equipped: true, icon: Shield },
    { id: 3, name: "Skórzane Buty", type: "boots", stats: "+2 Zręczność", equipped: true, icon: Boot },
    { id: 4, name: "Płócienna Zbroja", type: "armor", stats: "+4 Obrona", equipped: true, icon: Shirt },
    { id: 5, name: "Żelazny Miecz", type: "weapon", stats: "+8 Atak", equipped: false, icon: Sword },
    { id: 6, name: "Stalowa Tarcza", type: "shield", stats: "+7 Obrona", equipped: false, icon: Shield },
  ])

  const equipItem = (id: number) => {
    setItems(items.map((item) => (item.id === id ? { ...item, equipped: true } : item)))
  }

  const unequipItem = (id: number) => {
    setItems(items.map((item) => (item.id === id ? { ...item, equipped: false } : item)))
  }

  const equippedItems = items.filter((item) => item.equipped)
  const availableItems = items.filter((item) => !item.equipped)

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="bg-slate-800 rounded-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">Ekwipunek</h2>
          <div className="text-sm text-gray-400">Przeciągnij i upuść przedmioty, aby je założyć lub zdjąć</div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <DropArea onDrop={equipItem} title="Założone Przedmioty">
            {equippedItems.map((item) => (
              <DraggableItem key={item.id} item={item} onEquip={equipItem} onUnequip={unequipItem} isEquipped={true} />
            ))}
          </DropArea>

          <DropArea onDrop={unequipItem} title="Dostępne Przedmioty">
            {availableItems.map((item) => (
              <DraggableItem key={item.id} item={item} onEquip={equipItem} onUnequip={unequipItem} isEquipped={false} />
            ))}
          </DropArea>
        </div>
      </div>
    </DndProvider>
  )
}
