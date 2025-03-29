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
    {
      id: 1,
      choices: [
        { id: this.generateChoiceId(1, 1), label: 'Choix 1' },
        { id: this.generateChoiceId(1, 2), label: 'Choix 2' },
        { id: this.generateChoiceId(1, 3), label: 'Choix 3' }
      ],
      position: { x: 50, y: 50 },
      animate: true
    }
  ];
  lines: { line: any, linkedChoiceId: string }[] = [];
  occupiedPositions: Set<string> = new Set();

  @ViewChild('blockContainer', { static: false }) blockContainer!: ElementRef;

  ngAfterViewInit(): void {
    this.updateLines();

    setTimeout(() => {
      this.addChoiceHoverListeners();
    }, 150);
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
      position: { x, y },
      animate: true
    });

    this.occupiedPositions.add(positionKey);

    setTimeout(() => {
      this.updateLines();
      this.addChoiceHoverListeners();
    }, 50);
  }

  generateChoiceId(blockId: number, index: number): string {
    return `choice-${blockId}-${index}-${Math.floor(Math.random() * 100000)}`;
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
      position: { x, y },
      animate: true
    };

    this.blocks.push(newBlock);
    this.occupiedPositions.add(positionKey);

    setTimeout(() => {
      this.updateLines();
      this.addChoiceHoverListeners();
    }, 50);

    // Supprimer l'animation après qu'elle soit jouée
    setTimeout(() => {
      const b = this.blocks.find(b => b.id === newBlock.id);
      if (b) delete (b as any).animate;
    }, 1000);
      
  }

  updateLines() {
    this.lines.forEach(item => item.line.remove());
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
              endPlug: 'arrow2',
              startSocket: 'right',
              endSocket: 'left'
            });

            this.lines.push({ line, linkedChoiceId: (block as any).linkedChoiceId });
          }
        }
      });
    }, 100);
  }

  addChoiceHoverListeners() {
    this.blocks.forEach(block => {
      block.choices.forEach(choice => {
        const el = document.getElementById(choice.id);
        if (el) {
          el.addEventListener('mouseenter', () => this.highlightLine(choice.id));
          el.addEventListener('mouseleave', () => this.resetLine(choice.id));
        }
      });
    });
  }

  highlightLine(choiceId: string) {
    const item = this.lines.find(l => l.linkedChoiceId === choiceId);
    if (item) {
      item.line.setOptions({
        size: 6,
        color: '#FFD700',
        outline: true,
        outlineColor: '#f1f1f1'
      });
    }
  }

  resetLine(choiceId: string) {
    const item = this.lines.find(l => l.linkedChoiceId === choiceId);
    if (item) {
      const parentBlock = this.blocks.find(b => b.linkedChoiceId === choiceId);
      item.line.setOptions({
        size: 4,
        color: this.getColorForParent(parentBlock?.parentId || 0),
        outline: false
      });
    }
  }

  private parentColors = new Map<number, string>();

  private getColorForParent(parentId: number): string {
    if (!this.parentColors.has(parentId)) {
      const colors = [
        '#0078FF', '#00C6FF', '#00D563', '#FF7E67',
        '#FF3CAC', '#6F42C1', '#FFD700', '#FF6F91', '#17C3B2'
      ];
      const index = this.parentColors.size % colors.length;
      this.parentColors.set(parentId, colors[index]);
    }
    return this.parentColors.get(parentId)!;
  }

  getBlockBorderColor(block: Block): string {
    if (!block.parentId) {
      return 'black';
    }
    return this.getColorForParent(block.parentId);
  }
  
}
