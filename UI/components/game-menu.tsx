import { Button } from "@/components/ui/button"
import { Home, ShoppingBag, Swords, Trophy, Users, Settings } from "lucide-react"

export default function GameMenu() {
  return (
    <div className="grid grid-cols-3 gap-2 mb-4">
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <Home className="h-5 w-5 mb-1" />
        <span className="text-xs">Home</span>
      </Button>
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <ShoppingBag className="h-5 w-5 mb-1" />
        <span className="text-xs">Shop</span>
      </Button>
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <Swords className="h-5 w-5 mb-1" />
        <span className="text-xs">Battle</span>
      </Button>
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <Trophy className="h-5 w-5 mb-1" />
        <span className="text-xs">Quests</span>
      </Button>
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <Users className="h-5 w-5 mb-1" />
        <span className="text-xs">Guild</span>
      </Button>
      <Button variant="outline" className="flex flex-col h-16 bg-slate-800/60 border-slate-700 hover:bg-slate-700">
        <Settings className="h-5 w-5 mb-1" />
        <span className="text-xs">Settings</span>
      </Button>
    </div>
  )
}
