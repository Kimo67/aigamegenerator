import { Component, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { NgFor } from "@angular/common";
import { Block } from '../../core/models/block.model';

@Component({
  selector: 'app-block',
  standalone: true,
  imports: [NgFor],
  templateUrl: './block.component.html',
  styleUrls: ['./block.component.scss']
})
export class BlockComponent implements AfterViewInit {
  nextId = 2;
  blocks: Block[] = [
    { id: 1,
      choices: [
        { id: this.generateChoiceId(1, 1), label: 'Choix 1' },
        { id: this.generateChoiceId(1, 2), label: 'Choix 2' },
        { id: this.generateChoiceId(1, 3), label: 'Choix 3' }
      ],
      position: { x: 50, y: 50 }
    }
  ];  
  lines: any[] = [];
  occupiedPositions: Set<string> = new Set();

  @ViewChild('blockContainer', { static: false }) blockContainer!: ElementRef;

  ngAfterViewInit(): void {
    this.updateLines();
  }

  addBlock(parentId: number) {
    const parent = this.blocks.find(b => b.id === parentId);
    const siblings = this.blocks.filter(b => b.parentId === parentId);

    const baseX = (parent?.position?.x || 0) + 320;
    let baseY = (parent?.position?.y || 0);

    let yOffset = 0;
    let positionKey = `${baseX},${baseY + yOffset}`;

    while (this.occupiedPositions.has(positionKey)) {
      yOffset += 280;
      positionKey = `${baseX},${baseY + yOffset}`;
    }

    const x = baseX;
    const y = baseY + yOffset;

    this.blocks.push({
      id: this.nextId++,
      parentId,
      choices: [
        { id: this.generateChoiceId(this.nextId, 1), label: 'Choix 1' },
        { id: this.generateChoiceId(this.nextId, 2), label: 'Choix 2' },
        { id: this.generateChoiceId(this.nextId, 3), label: 'Choix 3' },
      ],
      position: { x, y }
    });

    this.occupiedPositions.add(positionKey);

    setTimeout(() => this.updateLines(), 50);
  }

  generateChoiceId(blockId: number, index: number): string {
    return `choice-${blockId}-${index}-${Date.now()}`;
  }  

  removeBlock(id: number) {
    this.blocks = this.blocks.filter(block => block.id !== id && block.parentId !== id);
    this.updateLines();
  }

  removeChoice(blockId: number, choiceId: string) {
    const block = this.blocks.find(b => b.id === blockId);
    if (!block) return;

    block.choices = block.choices.filter(c => c.id !== choiceId);

    const childBlock = this.blocks.find(
      b => b.parentId === blockId && b.linkedChoiceId === choiceId
    );
  
    if (childBlock) {
      this.removeBlockRecursive(childBlock.id);
    }
  
    this.updateLines();
  }

  removeBlockRecursive(id: number) {
    const children = this.blocks.filter(b => b.parentId === id);
    children.forEach(child => this.removeBlockRecursive(child.id));
  
    const block = this.blocks.find(b => b.id === id);
    if (block && block.position) {
      const key = `${block.position.x},${block.position.y}`;
      this.occupiedPositions.delete(key);
    }
  
    this.blocks = this.blocks.filter(b => b.id !== id);
  }  
  
  addBlockFromChoice(parentBlockId: number, choiceId: string) {
    const parent = this.blocks.find(b => b.id === parentBlockId);
    if (!parent) return;
    const alreadyLinked = this.blocks.some(
      b => b.parentId === parentBlockId && b.linkedChoiceId === choiceId
    );
    if (alreadyLinked) return;
  
    const baseX = (parent.position?.x || 0) + 320;
    let baseY = parent.position?.y || 0;
  
    let yOffset = 0;
    let positionKey = `${baseX},${baseY + yOffset}`;
    while (this.occupiedPositions.has(positionKey)) {
      yOffset += 280;
      positionKey = `${baseX},${baseY + yOffset}`;
    }
  
    const x = baseX;
    const y = baseY + yOffset;
  
    const newBlock: Block = {
      id: this.nextId++,
      parentId: parentBlockId,
      linkedChoiceId: choiceId,
      choices: [
        { id: this.generateChoiceId(this.nextId, 1), label: 'Choix 1' },
        { id: this.generateChoiceId(this.nextId, 2), label: 'Choix 2' },
        { id: this.generateChoiceId(this.nextId, 3), label: 'Choix 3' },
      ],
      position: { x, y }
    };
  
    this.blocks.push(newBlock);
    this.occupiedPositions.add(positionKey);
    setTimeout(() => this.updateLines(), 50);
  }    

  updateLines() {
    this.lines.forEach(line => line.remove());
    this.lines = [];
  
    setTimeout(() => {
      const LeaderLine = (window as any).LeaderLine;
  
      if (!LeaderLine) return;
  
      this.blocks.forEach(block => {
        if (block.parentId && (block as any).linkedChoiceId) {
          const parentChoiceElement = document.getElementById((block as any).linkedChoiceId);
          const childBlockElement = document.getElementById(`block-${block.id}`);
  
          if (parentChoiceElement && childBlockElement) {
            const line = new LeaderLine(parentChoiceElement, childBlockElement, {
              path: 'fluid',
              color: this.getColorForParent(block.parentId),
              size: 4,
              dash: { animation: true },
              startPlug: 'disc',
              endPlug: 'arrow2'
            });            
            this.lines.push(line);
          }
        }
      });
    }, 100);
  }  

  private parentColors = new Map<number, string>();

  private getColorForParent(parentId: number): string {
    if (!this.parentColors.has(parentId)) {
      const colors = [
        '#0078FF', // bleu
        '#00C6FF', // cyan
        '#00D563', // vert clair
        '#FF7E67', // orange pastel
        '#FF3CAC', // rose
        '#6F42C1', // violet
        '#FFD700', // jaune or
        '#FF6F91', // rose doux
        '#17C3B2'  // turquoise
      ];
      const index = this.parentColors.size % colors.length;
      this.parentColors.set(parentId, colors[index]);
    }
    return this.parentColors.get(parentId)!;
  }

}