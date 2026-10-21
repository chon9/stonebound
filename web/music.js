// One persistent audio element survives navigation, dialogue and state polling.
export class MusicPlayer {
  constructor(onChange = () => {}) {
    this.audio = document.createElement('audio');
    this.audio.id = 'bgm-audio';
    this.audio.preload = 'metadata';
    this.audio.hidden = true;
    document.body.append(this.audio);
    this.onChange = onChange;
    this.tracks = [];
    this.track = null;
    this.enabled = true;
    this.volume = .22;
    this.unlocked = false;
    this.blocked = false;
    this.failed = new Set();
    this.saved = {};
    this.playAttempt = 0;
    this.audio.addEventListener('ended', () => this.next());
    this.audio.addEventListener('error', () => this.recover());
    for (const event of ['playing', 'pause', 'waiting', 'loadedmetadata']) {
      this.audio.addEventListener(event, () => this.notify());
    }
    const unlock = event => {
      if (!event.isTrusted || this.unlocked && !this.blocked) return;
      this.unlocked = true;
      this.blocked = false;
      // A first click on mute should never start a short burst of music.
      if (this.enabled && !event.target.closest?.('[data-action="music"],[data-action="music-settings"]')) {
        void this.play();
      }
    };
    document.addEventListener('pointerdown', unlock, {capture: true});
    document.addEventListener('keydown', unlock, {capture: true});
  }

  configure(profile, tracks) {
    this.tracks = tracks || [];
    const enabled = profile.music !== false;
    const volume = Number.isFinite(profile.music_volume) ? Math.max(0, Math.min(1, profile.music_volume)) : .22;
    const id = profile.music_track || this.tracks[0]?.id;
    const justEnabled = enabled && !this.enabled;
    this.enabled = enabled;
    if (volume !== this.saved.volume) this.setVolume(volume);
    // Automatic song changes stay in place when the game polls its saved state.
    if (id !== this.saved.track || !this.track) this.select(id);
    this.saved = {volume, track: id};
    if (!enabled) {
      this.playAttempt++;
      this.audio.pause();
    } else if (justEnabled && this.unlocked) {
      void this.play();
    }
    this.notify();
  }

  select(id, retry = true) {
    const track = this.tracks.find(t => t.id === id) || this.tracks[0];
    if (!track) return;
    if (retry) this.failed.delete(track.id);
    if (this.track?.id === track.id && !this.audio.error && !this.audio.ended) return;
    this.playAttempt++;
    this.audio.pause();
    this.track = track;
    this.audio.src = track.file;
    this.audio.volume = this.volume;
    this.audio.load();
    if (this.enabled && this.unlocked) void this.play();
    this.notify();
  }

  next(direction = 1) {
    if (!this.tracks.length) return;
    const index = this.tracks.findIndex(t => t.id === this.track?.id);
    for (let n = 1; n <= this.tracks.length; n++) {
      const track = this.tracks[((index + direction * n) % this.tracks.length + this.tracks.length) % this.tracks.length];
      if (!this.failed.has(track.id)) {
        this.select(track.id, false);
        return;
      }
    }
    this.notify();
  }

  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume));
    this.audio.volume = this.volume;
    this.notify();
  }

  async play() {
    if (!this.enabled || !this.unlocked || !this.track || this.failed.size >= this.tracks.length) return;
    const attempt = ++this.playAttempt;
    try {
      await this.audio.play();
      if (attempt !== this.playAttempt) return;
      this.blocked = false;
    } catch (error) {
      if (attempt !== this.playAttempt || error.name === 'AbortError') return;
      this.blocked = error.name === 'NotAllowedError';
      // Decode/network failures use the media error handler and try another song.
    }
    this.notify();
  }

  recover() {
    if (!this.track) return;
    this.failed.add(this.track.id);
    this.next();
  }

  notify() {
    this.onChange(this);
  }

  get unavailable() {
    return this.tracks.length > 0 && this.failed.size >= this.tracks.length;
  }

  get playing() {
    return !this.audio.paused && !this.audio.ended && !this.audio.error;
  }
}
