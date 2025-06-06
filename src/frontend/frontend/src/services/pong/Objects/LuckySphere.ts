import {
  Color,
  Mesh,
  MeshBasicMaterial,
  SphereGeometry,
  Vector3,
  Sphere as ThreeSphere
} from 'three'
import Sphere from './Sphere'
import type Player from './Player'

export default class LuckySphere {
  protected mesh: Mesh
  protected material: MeshBasicMaterial
  protected geometry: SphereGeometry

  constructor(vector: Array<number>, color: Color) {
    this.geometry = new SphereGeometry(vector[0], vector[1], vector[2])
    this.material = new MeshBasicMaterial({ color })
    this.mesh = new Mesh(this.geometry, this.material)
    this.randomizePosition()
  }

  public get(): Mesh {
    return this.mesh
  }

  public randomizePosition(): void {
    this.mesh.position.x = Math.random() * 10
    this.mesh.position.y = Math.random() * 8

    const ranAxis = Math.random()
    if (ranAxis <= 0.5) {
      this.mesh.position.x = -this.mesh.position.x
      this.mesh.position.y = -this.mesh.position.y
    }
  }

  private applyEffects(ball: Sphere, player: Player): void {
    let random = Math.random() * 5
    random = Math.floor(random)

    switch (random) {
      case 0:
        ball.speedUp(0.3)
        break
      case 1:
        /* Slow downs the ball to half of its speed */
        ball.speedUp((Math.abs(ball.getSpeed() / 2)) * -1)
        break
      case 2:
        ball.resize((Math.random() * 5) + 1.5)
        break
      case 3:
        ball.resize((Math.random() * 0.20) + 0.25)
        break
      case 4:
        player.resize((Math.random() * 0.20) + 0.25)
        break
      case 5:
        player.resize((Math.random() * 5) + 1.5)
        break
      default:
        break
    }
  }

  private timeElapsed: number = 0

  public update(ball: Sphere, player: Player): number {
    const now = Date.now()

    if (this.intersects(ball) && now - this.timeElapsed > 5000) {
      this.timeElapsed = now
      this.applyEffects(ball, player)
      return 1
    } else {
      const randomColor = new Color(Math.random(), Math.random(), Math.random())
      this.material.color = randomColor
      return 0
    }
  }

  // Create a bounding sphere for collision detection
  public getBoundingSphere(): ThreeSphere {
    // Assume the sphere radius is the same as its geometry's radius
    const radius = (this.geometry as SphereGeometry).parameters.radius
    return new ThreeSphere(this.mesh.position, radius)
  }

  // Check if this sphere intersects with another sphere
  public intersects(other: Sphere): boolean {
    const thisSphere = this.getBoundingSphere()
    const otherSphere = other.getBoundingSphere()
    return thisSphere.intersectsSphere(otherSphere)
  }

  public setPosition(pos: Vector3) {
    this.mesh.position.x = pos.x
    this.mesh.position.y = pos.y
    this.mesh.position.z = pos.z
  }

  dispose(): void {
    // Dispose of geometry and material
    if (this.mesh.geometry) this.mesh.geometry.dispose()
    if (this.mesh.material) {
      if (Array.isArray(this.mesh.material)) {
        this.mesh.material.forEach((mat) => mat.dispose())
      } else {
        this.mesh.material.dispose()
      }
    }
  }
}
