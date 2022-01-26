import { Area } from "./class.area";
import { Coord } from "./class.coord";
export declare class Selection {
    protected origin: Coord;
    protected position: Coord;
    protected areas: Map<number, Area>;
    protected points: Map<Coord, number>;
    constructor();
    resetOrigin(coord?: Coord): void;
    /**
     * Register an Area as a part of the selection
     */
    registerArea(area: Area): void;
    /**
     * Add Area and its points to the selection
     */
    addArea(area: Area): void;
    addPoint(point: Coord): void;
    containsArea(area: Area): boolean;
    containsPoint(point: Coord): boolean;
    distToOrigin(): Coord;
    clear(): void;
    isEmpty(): boolean;
    move(coord: Coord): void;
    getPosition(): Coord;
    setPosition(coord: Coord): void;
}
