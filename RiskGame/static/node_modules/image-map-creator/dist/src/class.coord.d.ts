import { Movable } from "./interface.movable";
declare type Axle = "x" | "y";
/**
 * Class representing a 2d xy coordinate
*/
export declare class Coord implements Movable {
    x: number;
    y: number;
    constructor(x?: number, y?: number);
    set(x: number, y: number): this;
    static fromObject(obj: Object): Coord;
    /**
     * returns the distance between two xy coordinates
     * @param {Coord} coord1
     * @param {Coord} coord2
     */
    static dist(coord1: Coord, coord2: Coord): number;
    /**
     * Exchanges a value between two xy coordinates
     * @param {Coord} coord1
     * @param {Coord} coord2
     * @param {Axle} val
     */
    static swap(coord1: Coord, coord2: Coord, val: Axle): void;
    isEmpty(): boolean;
    oneIsEmpty(): boolean;
    /**
     * returns the sum of two xy coordinates
     * @param {Coord} coord
     */
    sum(coord: Coord): Coord;
    /**
     * Add the value of the given coordinate to the current one
     * @param {Coord} coord
     */
    add(coord: Coord): this;
    /**
     * returns the difference of two xy coordinates
     * @param {Coord} coord
     */
    diff(coord: Coord): Coord;
    /**
     * Substract the value of the given coordinate to the current one
     * @param {Coord} coord
     */
    sub(coord: Coord): this;
    /**
     * Alias of add
     * @param {Coord} coord
     */
    move(coord: Coord): void;
    getPosition(): Coord;
    setPosition(coord: Coord): this;
    clone(): Coord;
    invert(): Coord;
    toStr(dec: number, val: Axle, scale: number): string;
    toHtml(dec: number, scale?: number): string;
}
export {};
