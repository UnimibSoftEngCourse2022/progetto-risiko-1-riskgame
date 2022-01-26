import { Coord } from "./class.coord";
import { ImageMap } from "./class.image-map";
import * as p5 from "p5";
export declare type Shape = "empty" | "rect" | "circle" | "poly" | "default";
export declare abstract class Area {
    protected shape: Shape;
    protected coords: Coord[];
    protected href: string;
    protected title: string;
    id: number;
    /**
     * @param {Shape} shape the type of area
     * @param {Coord[]} coords the list of coordinates
     * @param {string} href the link this area is going to point to
     * @param {number} id the unique id
     */
    constructor(shape: Shape, coords?: Coord[], href?: string, title?: string, id?: number);
    static fromObject(o: Object): Area;
    getId(): number;
    setShape(shape: Shape): this;
    getShape(): Shape;
    /**
     * Adds a coordinate to the coords array, and returns it's new length
     * @param {Coord} coord coordinate
     */
    addCoord(coord: Coord): number;
    setCoords(coords: Coord[]): this;
    getCoords(): Coord[];
    /**
     * Returns a copy of this area's coordinates list
     */
    drawingCoords(): Coord[];
    getPoints(): Coord[];
    isEmpty(): boolean;
    /**
     * @param {Area} area
     */
    equals(area: Area): boolean;
    /**
     * Retuns a deep copy of this area's coordinates
     */
    copyCoords(): Coord[];
    updateLastCoord(coord: Coord): this;
    move(coord: Coord): void;
    getPosition(): Coord;
    setPosition(coord: Coord): void;
    isValidShape(): boolean;
    /**
     * @param {Coord} coord
     * @param {number} tolerance
     * @returns {Coord|false}
     */
    isOverPoint(coord: Coord, tolerance: number): Coord | false;
    setHref(url: string): this;
    getHref(): string;
    getHrefVerbose(): string;
    setTitle(title: string): this;
    getTitle(): string;
    setId(id: number): this;
    firstCoord(): Coord;
    htmlCoords(dec: number, scale: number): string;
    toHtml(scale?: number): string;
    toSvg(scale?: number): string;
    abstract isDrawable(): boolean;
    abstract svgArea(scale: number): string;
    abstract isOver(coord: Coord): boolean;
    abstract display(p: p5): void;
}
export declare class AreaEmpty extends Area {
    constructor();
    isDrawable(): boolean;
    svgArea(scale: number): string;
    isOver(coord: Coord): boolean;
    display(p: p5): void;
}
export declare class AreaCircle extends Area {
    radius: number;
    /**
     * @param {Coord[]} coords the list of coordinates
     * @param {number} radius radius of the circle
     * @param {string} href the link this area is going to point to
     * @param {number} id the unique id
     */
    constructor(coords?: Coord[], radius?: number, href?: string, title?: string, id?: number);
    getCenter(): Coord;
    isValidShape(): boolean;
    isDrawable(): boolean;
    isOver(coord: Coord): boolean;
    updateLastCoord(coord: Coord): this;
    /**
     * draw the area to the given p5 instance
     * @param {p5} p5
     */
    display(p5: p5): void;
    htmlCoords(dec: number, scale: number): string;
    svgArea(scale: number): string;
}
export declare class AreaPoly extends Area {
    closed: boolean;
    /**
     * @param {Coord[]} coords the list of coordinates
     * @param {string} href the link this area is going to point to
     * @param {int} id the unique id
     */
    constructor(coords?: Coord[], href?: string, title?: string, id?: number, closed?: boolean);
    isDrawable(): boolean;
    isValidShape(): boolean;
    isOver(coord: Coord): boolean;
    isClosable(coord: Coord, tolerance: number): boolean;
    drawingCoords(): Coord[];
    close(): this;
    move(coord: Coord): void;
    /**
     * draw the area to the given p5 instance
     * @param {p5} p5
     */
    display(p5: p5): void;
    svgArea(scale: number): string;
}
export declare class AreaRect extends AreaPoly {
    /**
     * @param {Coord[]} coords the list of coordinates
     * @param {string} href the link this area is going to point to
     * @param {number} id the unique id
     */
    constructor(coords?: Coord[], href?: string, title?: string, id?: number);
    isValidShape(): boolean;
    private isNullArea;
    updateLastCoord(coord: Coord): this;
}
export declare class AreaDefault extends Area {
    iMap: ImageMap;
    protected isDefault: boolean;
    /**
     * Constructor
     * @param {string} href the link this area is going to point to
     * @param {string} title the title on hover
     */
    constructor(iMap: ImageMap, href?: string, title?: string);
    isDrawable(): boolean;
    isOver(): boolean;
    /**
     * draw the area to the given p5 instance
     * @param {p5} p5
     */
    display(p5: p5): void;
    svgArea(scale: number): string;
}
