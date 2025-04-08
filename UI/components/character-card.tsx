import Image from "next/image"
import { Card, CardContent } from "@/components/ui/card"

export default function CharacterCard() {
  return (
    <Card className="bg-slate-800/60 border-slate-700 overflow-hidden">
      <div className="bg-gradient-to-r from-purple-800 to-purple-600 p-3 text-center">
        <h2 className="font-bold text-xl">Sir Laughalot</h2>
        <p className="text-sm text-slate-200">Warrior - Level 12</p>
      </div>
      <CardContent className="p-0">
        <div className="flex justify-center bg-slate-900/50 py-4">
          <div className="relative w-40 h-48">
            <Image
              src="/placeholder.svg?height=192&width=160"
              alt="Character"
              width={160}
              height={192}
              className="object-contain"
            />
          </div>
        </div>
        <div className="p-4 text-center">
          <p className="text-sm text-slate-300">Guild: The Merry Pranksters</p>
          <p className="text-sm text-slate-300">Battles won: 42</p>
        </div>
      </CardContent>
    </Card>
  )
}
