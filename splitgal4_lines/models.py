from django.db import models
from django.utils import timezone
class fly_line(models.Model):
    EFFECTORS = [
        ("DBD", "DNA-binding domain"),
        ("AD", "Activation domain"),
    ]
    ACTIVATORS = [
        ("VP16", "VP16 activation domain"),
        ("p65", "p65 activation domain"),
        ("GAL4AD", "GAL4 activation domain"),
        ("AD", "Unknown activation domain")
    ]
    CASSETTE_STYLE = [
        ("C-term", "C-terminus tagging"),
        ("N-term", "N-terminus tagging"),
        ("SA", "Gene trap with 5' splicing acceptors"),
    ]

    DIMERIZER_STYLE = [
        ("zip", "Leucine zipper"),
        ("int", "Intein")
    ]

    STATUS_LIST = [
        ("val", "Available (Validated)"),
        ("ava", "Available (Not validated)"),
        ("inp", "In progress"),
        ("req", "Planned")
    ]

    CHRS = [
        ("chrX", "chromosome X"),
        ("chr2R", "chromosome 2R"),
        ("chr2L", "chromosome 2L"),
        ("chr3R", "chromosome 3R"),
        ("chr3L", "chromosome 3L"),
        ("chr4", "chromosome 4"),
    ]

    gene_name = models.CharField(max_length=128, blank=False)
    effector_type = models.CharField(
        max_length=3,
        choices=EFFECTORS,
        blank=False
    )
    activator_type = models.CharField(
        max_length=6,
        choices=ACTIVATORS,
        blank=True,
        default="NA"
    )
    source_id = models.CharField(
        max_length=16,
        blank=True,
        default=""
    )
    cassette = models.CharField(
        max_length=8,
        choices=CASSETTE_STYLE,
        blank=False
    )
    dimerizer = models.CharField(
        max_length=8,
        choices=DIMERIZER_STYLE,
        blank=False,
        default="zip"
    )
    ins_seqname = models.CharField(
       max_length=8,
       choices=CHRS,
       blank=True,
       default=""
    )
    ins_site = models.BigIntegerField(
        blank=True,
        default=-1
    )
    contributor = models.CharField(
        max_length=256, blank=False, default="Anonymous"
    )
    uploader = models.CharField(
        max_length=256, blank=False, default="Anonymous"
    )
    reference = models.CharField(max_length=1024, blank=True, default="")
    status = models.CharField(
        max_length=4,
        blank=False,
        default="ava",
        choices=STATUS_LIST
    )
    internal_sharing = models.BooleanField(default=False, blank=False)
    need_review = models.BooleanField(default=False, blank=False)
    date_created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.gene_name + '-' + self.effector_type

