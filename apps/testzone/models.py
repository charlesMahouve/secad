from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class TestCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    run_by = models.ForeignKey(User, related_name='TestCategories', on_delete=models.CASCADE)
    run_at = models.DateTimeField(auto_now_add=True)
    run_in = models.TimeField(blank=True, null=True)
    forest_mode = models.CharField(max_length=50, null=True)
    schema_master = models.CharField(max_length=50, null=True)
    operating_system = models.CharField(max_length=50, null=True)
    enabled = models.CharField(max_length=50, null=True)
    schema_version = models.CharField(max_length=50, null=True)
    present = models.CharField(max_length=50, null=True)
    servers = models.CharField(max_length=50, null=True)
    sid_filtering_forest_aware = models.CharField(max_length=50, null=True)
    sid_filtering_quarantined = models.CharField(max_length=50, null=True)
    tgt_delegation = models.CharField(max_length=50, null=True)
    domain_mode = models.CharField(max_length=50, null=True)
    infrastructure_master = models.CharField(max_length=50, null=True)
    pdc_emulator = models.CharField(max_length=50, null=True)
    rid_master = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    password_history_count = models.CharField(max_length=50, null=True)
    max_password_age = models.CharField(max_length=50, null=True)
    min_password_age = models.CharField(max_length=50, null=True)
    reversible_encryption_enabled = models.CharField(max_length=50, null=True)
    complexity_enabled = models.CharField(max_length=50, null=True)
    min_password_length = models.CharField(max_length=50, null=True)
    lockout_duration = models.CharField(max_length=50, null=True)
    lockout_observation_window = models.CharField(max_length=50, null=True)
    lockout_threshold = models.CharField(max_length=50, null=True)
    applies_to = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    protected_from_accidental_deletion = models.CharField(max_length=50, null=True)
    gpo_inheritance_blocked = models.CharField(max_length=50, null=True)
    groups_with_sid_history = models.CharField(max_length=50, null=True)
    members1 = models.CharField(max_length=50, null=True)
    members2 = models.CharField(max_length=50, null=True)
    users = models.CharField(max_length=50, null=True)
    groups = models.CharField(max_length=50, null=True)
    global_groups = models.CharField(max_length=50, null=True)
    universal_groups = models.CharField(max_length=50, null=True)
    modification_time = models.CharField(max_length=50, null=True)
    enabled = models.CharField(max_length=50, null=True)
    enforced = models.CharField(max_length=50, null=True)
    check_type = models.CharField(max_length=50, null=True)
    all_users_whose_password_never_expires = models.CharField(max_length=50, null=True)
    all_users_with_password_not_required = models.CharField(max_length=50, null=True)
    all_users_who_cannot_change_password = models.CharField(max_length=50, null=True)
    all_users_with_sid_history = models.CharField(max_length=50, null=True)
    all_users_with_bad_primary_group = models.CharField(max_length=50, null=True)
    active_users_whose_password_never_expires = models.CharField(max_length=50, null=True)
    active_users_whose_password_not_required = models.CharField(max_length=50, null=True)
    active_users_who_cannot_change_password = models.CharField(max_length=50, null=True)
    member_of = models.CharField(max_length=50, null=True)
    password_last_set = models.CharField(max_length=50, null=True)
    password_never_expires = models.CharField(max_length=50, null=True)
    password_not_required = models.CharField(max_length=50, null=True)
    display_name = models.CharField(max_length=50, null=True)
    links_to_enabled = models.CharField(max_length=50, null=True)
    gpo_status = models.CharField(max_length=50, null=True)
    computer_extension_datas = models.CharField(max_length=50, null=True)
    user_extension_data = models.CharField(max_length=50, null=True)
    computer_sys_vol_version = models.CharField(max_length=50, null=True)
    user_sys_vol_version = models.CharField(max_length=50, null=True)
    os_version = models.CharField(max_length=50, null=True)
    activate = models.CharField(max_length=50, null=True)
    operating_systems = models.CharField(max_length=50, null=True)
    maximum_kilo_bytes = models.CharField(max_length=50, null=True)
    total_physical_memory = models.CharField(max_length=50, null=True)
    bios = models.CharField(max_length=50, null=True)
    free_spaces = models.CharField(max_length=50, null=True)
    dhcp_enabled = models.CharField(max_length=50, null=True)
    tcpi_net_bios_options = models.CharField(max_length=50, null=True)
    enabled3 = models.CharField(max_length=50, null=True)
    transport = models.CharField(max_length=50, null=True)
    name1 = models.CharField(max_length=50, null=True)
    install_state = models.CharField(max_length=50, null=True)
    user_authentication_required = models.CharField(max_length=50, null=True)
    scavenging_state = models.CharField(max_length=50, null=True)
    ip_address = models.CharField(max_length=50, null=True)
    replication_scope = models.CharField(max_length=50, null=True)
    is_ds_intergrated = models.CharField(max_length=50, null=True)
    is_shutdown = models.CharField(max_length=50, null=True)
    aging_enabled = models.CharField(max_length=50, null=True)
    test_results = models.CharField(max_length=50, null=True)
    deletion = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name_plural = 'TestCategories'

    def __str__(self):
        return self.title
