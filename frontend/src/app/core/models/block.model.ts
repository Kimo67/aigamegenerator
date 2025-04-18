export interface Block {
    id: number;
    parentId?: number;
    linkedChoiceId?: string;
    choices: { id: string; label: string }[];
    position?: { x: number; y: number };
    command?: string;
}
  