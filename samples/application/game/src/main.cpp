#include "SkrRT/module/module_manager.hpp"
#include "SkrRT/platform/filesystem.hpp"
#include "SkrRT/misc/log.h"
#include "SkrRT/async/fib_task.hpp"

#include "tracy/Tracy.hpp"

int main(int argc, char** argv)
{
    ZoneScopedN("Main");

    auto moduleManager = skr_get_module_manager();
    std::error_code ec = {};
    auto root = skr::filesystem::current_path(ec);
    moduleManager->mount(root.u8string().c_str());
    moduleManager->make_module_graph(u8"Game", true);
    auto result = moduleManager->init_module_graph(argc, argv);
    if (result != 0) {
        SKR_LOG_ERROR(u8"module graph init failed!");
    }
    moduleManager->destroy_module_graph();
    return 0;
}