from dissect.cstruct import cstruct

c_thumbcache_index_def = """
struct INDEX_HEADER_V1 {
  char   signature[4];
  uint32 version;
  uint32 unknown1;
  uint32 used_entries;
  uint32 total_entries;
  uint32 unknown2;
};

struct INDEX_HEADER_V2 {
  char   signature[8];  // 0x00
  uint64 version;       // 0x08
  uint32 unknown1;      // 0x10
  uint32 used_entries;  // 0x14
  uint32 total_entries; // 0x18
  uint32 unknown2;      // 0x1B
}; // 0x20

struct VISTA_ENTRY {
    char hash[8];
    uint64 last_modified;
    uint32 flags;
};

struct WINDOWS7_ENTRY {
    char hash[8];
    uint32 flags;
};

struct WINDOWS8_ENTRY {
    char hash[8];
    uint32 flags;
    uint32 unknown; // Is sometims filled with information, couldn't figure out what it meant yet though.
}

struct CACHE_HEADER {
    char   signature[4];
    uint32 version;
    uint32 type;
    uint32 size;
    uint32 offset;
    uint32 entries;
}

struct CACHE_HEADER_VISTA {
    char   signature[4];
    uint32 version;
    uint32 type;
    uint32 offset;
    uint32 size;
    uint32 entries;
}

struct CACHE_ENTRY {
    char   signature[4];
    uint32 size;
    char   hash[8];
    uint32 identifier_size;
    uint32 padding_size;
    uint32 data_size;
    uint32 _unknown3;
}

struct CACHE_ENTRY_VISTA {
    char   signature[4];
    uint32 size;
    char   hash[8];
    wchar  extension[4];
    uint32 identifier_size;
    uint32 padding_size;
    uint32 data_size;
    uint32 _unknown3;
}
"""
c_thumbcache_index = cstruct()
c_thumbcache_index.load(c_thumbcache_index_def)
