#pragma once
#include "SkrRT/module/module.hpp"
#include "SkrRT/platform/shared_library.hpp"
#include "SkrRT/platform/dstorage.h"
#ifdef _WIN32
#include "SkrRT/platform/win/dstorage_windows.h"
#endif

class SKR_RUNTIME_API SkrRuntimeModule : public skr::IDynamicModule
{
public:
    virtual void on_load(int argc, char8_t** argv) override;
    virtual void on_unload() override;

    static SkrRuntimeModule* Get();

    bool DPIAware = false;
    skr::SharedLibrary tracyLibrary;
    SkrDStorageInstanceId dstorageInstance = nullptr;
#ifdef _WIN32
    skr_win_dstorage_decompress_service_id dstroageDecompressService = nullptr;
#endif
};

SKR_EXTERN_C SKR_RUNTIME_API bool skr_runtime_is_dpi_aware();
SKR_EXTERN_C SKR_RUNTIME_API SkrDStorageInstanceId skr_runtime_get_dstorage_instance();
SKR_EXTERN_C SKR_RUNTIME_API void skr_runtime_free_dstorage_instance();

#ifdef _WIN32
SKR_EXTERN_C SKR_RUNTIME_API skr_win_dstorage_decompress_service_id 
skr_runtime_create_win_dstorage_decompress_service(const skr_win_dstorage_decompress_desc_t* desc);

SKR_EXTERN_C SKR_RUNTIME_API skr_win_dstorage_decompress_service_id 
skr_runtime_get_win_dstorage_decompress_service();
#endif
