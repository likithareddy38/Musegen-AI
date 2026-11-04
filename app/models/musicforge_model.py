
import torch
import torch.nn as nn

LATENT_DIM = 128
NUM_TRACKS = 3
NUM_PITCHES = 88
NUM_STEPS = 32


class MusicForgeGenerator(nn.Module):

    def __init__(self, latent_dim=128):
        super().__init__()

        self.latent_dim = latent_dim

        self.shared = nn.Sequential(
            nn.Linear(latent_dim, 256 * 11 * 4),
            nn.BatchNorm1d(256 * 11 * 4),
            nn.ReLU(True)
        )

        self.upsampling = nn.Sequential(
            nn.Unflatten(1, (256, 11, 4)),

            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),

            nn.ConvTranspose2d(128, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),

            nn.ConvTranspose2d(64, 32, 4, 2, 1),
            nn.BatchNorm2d(32),
            nn.ReLU(True)
        )

        self.track_heads = nn.ModuleList([
            nn.Conv2d(32, 1, kernel_size=1)
            for _ in range(NUM_TRACKS)
        ])

    def forward(self, z):
        x = self.shared(z)
        x = self.upsampling(x)

        tracks = [head(x) for head in self.track_heads]

        return torch.cat(tracks, dim=1)


class MusicForgeDiscriminator(nn.Module):

    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(NUM_TRACKS, 32, 4, 2, 1),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(32, 64, 4, 2, 1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(64, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 11 * 4, 1)
        )

    def forward(self, x):
        features = self.features(x)
        return self.classifier(features)
